import { expect } from "chai";
import hre from "hardhat";
const { ethers } = hre;

// Helper function to convert bytes32 to string
function bytes32ToString(bytes32) {
  return ethers.decodeBytes32String(bytes32);
}

describe("CyberdyneMarketplace", function () {
  let CyberdyneMarketplace, CyberdyneProducts, CyberdyneAccessNFT, MockUSDC;
  let marketplace, products, accessNFT, usdcToken;
  let owner, seller, buyer, admin, feeRecipient, unauthorized;

  // Constants
  const MARKETPLACE_FEE_PERCENT = 250; // 2.5%
  const USDC_DECIMALS = 6;
  const INITIAL_USDC_SUPPLY = ethers.parseUnits("1000000", USDC_DECIMALS); // 1M USDC
  const PRODUCT_PRICE = ethers.parseUnits("100", USDC_DECIMALS); // 100 USDC

  beforeEach(async function () {
    // Get signers
    [owner, seller, buyer, admin, feeRecipient, unauthorized] = await ethers.getSigners();

    // Deploy Mock USDC token
    MockUSDC = await ethers.getContractFactory("MockERC20");
    usdcToken = await MockUSDC.deploy(INITIAL_USDC_SUPPLY);
    await usdcToken.waitForDeployment();

    // Deploy CyberdyneAccessNFT
    CyberdyneAccessNFT = await ethers.getContractFactory("CyberdyneAccessNFT");
    accessNFT = await CyberdyneAccessNFT.deploy(
      "Cyberdyne Access Pass",
      "CYBACC",
      "https://api.cyberdyne.xyz/metadata/"
    );
    await accessNFT.waitForDeployment();

    // Deploy CyberdyneProducts
    CyberdyneProducts = await ethers.getContractFactory("CyberdyneProducts");
    products = await CyberdyneProducts.deploy();
    await products.waitForDeployment();

    // Deploy CyberdyneMarketplace
    CyberdyneMarketplace = await ethers.getContractFactory("CyberdyneMarketplace");
    marketplace = await CyberdyneMarketplace.deploy(
      await usdcToken.getAddress(),
      await products.getAddress(),
      await accessNFT.getAddress(),
      MARKETPLACE_FEE_PERCENT,
      feeRecipient.address
    );
    await marketplace.waitForDeployment();

    // Setup permissions: Authorize seller in products
    await products.authorizeCreator(seller.address);

    // Mint marketplace access NFT to seller
    await accessNFT.mint(
      seller.address,
      false, // learningMaterials
      false, // frontendServers
      false, // backendServers
      false, // blogCreator
      false, // admin
      true,  // canSellMarketplace
      ""     // metadataURI
    );

    // Create categories
    await products.connect(seller).createCategory("Electronics", "Electronic products");

    // Setup USDC balances and allowances
    await usdcToken.transfer(buyer.address, ethers.parseUnits("10000", USDC_DECIMALS));
    await usdcToken.connect(buyer).approve(await marketplace.getAddress(), ethers.parseUnits("10000", USDC_DECIMALS));
  });

  describe("Deployment", function () {
    it("Should set the correct contract addresses", async function () {
      expect(await marketplace.usdcToken()).to.equal(await usdcToken.getAddress());
      expect(await marketplace.cyberdyneProducts()).to.equal(await products.getAddress());
      expect(await marketplace.accessNFT()).to.equal(await accessNFT.getAddress());
    });

    it("Should set the correct marketplace parameters", async function () {
      expect(await marketplace.marketplaceFeePercent()).to.equal(MARKETPLACE_FEE_PERCENT);
      expect(await marketplace.feeRecipient()).to.equal(feeRecipient.address);
      expect(await marketplace.marketplaceActive()).to.be.true;
    });

    it("Should initialize with correct starting values", async function () {
      expect(await marketplace.nextListingId()).to.equal(1);
      expect(await marketplace.nextSaleId()).to.equal(1);
      expect(await marketplace.getActiveListingsCount()).to.equal(0);
    });
  });

  describe("Product Listing", function () {
    let productId;

    beforeEach(async function () {
      // Create a product
      const tx1 = await products.connect(seller).createProduct(
        "Test Product",
        1, // categoryId
        PRODUCT_PRICE,
        "QmTestIPFS"
      );
      const receipt1 = await tx1.wait();
      productId = receipt1.logs[0].args.productId;
    });

    it("Should allow authorized seller to list product", async function () {
      const tx = await marketplace.connect(seller).listProduct(productId);
      const receipt = await tx.wait();
      
      expect(receipt.logs).to.not.be.empty;
      expect(await marketplace.getActiveListingsCount()).to.equal(1);
      expect(await marketplace.isProductListed(productId)).to.be.true;
    });

    it("Should reject listing from unauthorized user", async function () {
      await expect(
        marketplace.connect(unauthorized).listProduct(productId)
      ).to.be.revertedWith("Not authorized to sell on marketplace");
    });

    it("Should reject listing non-existent product", async function () {
      await expect(
        marketplace.connect(seller).listProduct(999)
      ).to.be.revertedWith("Product does not exist");
    });

    it("Should reject duplicate listing", async function () {
      await marketplace.connect(seller).listProduct(productId);
      
      await expect(
        marketplace.connect(seller).listProduct(productId)
      ).to.be.revertedWith("Product already listed");
    });

    it("Should allow owner to list products", async function () {
      await marketplace.connect(owner).listProduct(productId);
      expect(await marketplace.isProductListed(productId)).to.be.true;
    });
  });

  describe("Listing Management", function () {
    let listingId, productId;

    beforeEach(async function () {
      // Create and list a product
      const tx1 = await products.connect(seller).createProduct(
        "Test Product",
        1,
        PRODUCT_PRICE,
        "QmTestIPFS"
      );
      const receipt1 = await tx1.wait();
      productId = receipt1.logs[0].args.productId;

      const tx2 = await marketplace.connect(seller).listProduct(productId);
      const receipt2 = await tx2.wait();
      listingId = receipt2.logs[0].args.listingId;
    });

    it("Should allow seller to update listing price", async function () {
      const newPrice = ethers.parseUnits("150", USDC_DECIMALS);
      
      await marketplace.connect(seller).updateListingPrice(listingId, newPrice);
      
      const listing = await marketplace.getActiveListing(listingId);
      expect(listing.priceUSDC).to.equal(newPrice);
    });

    it("Should allow seller to unlist product", async function () {
      await marketplace.connect(seller).unlistProduct(listingId);
      
      expect(await marketplace.isProductListed(productId)).to.be.false;
      expect(await marketplace.getActiveListingsCount()).to.equal(0);
    });

    it("Should reject price update from unauthorized user", async function () {
      await expect(
        marketplace.connect(unauthorized).updateListingPrice(listingId, PRODUCT_PRICE)
      ).to.be.revertedWith("Only seller, admin, or owner can update price");
    });

    it("Should reject zero price update", async function () {
      await expect(
        marketplace.connect(seller).updateListingPrice(listingId, 0)
      ).to.be.revertedWith("Price must be greater than 0");
    });
  });

  describe("Product Purchase", function () {
    let listingId, productId;

    beforeEach(async function () {
      // Create and list a product
      const tx1 = await products.connect(seller).createProduct(
        "Test Product",
        1,
        PRODUCT_PRICE,
        "QmTestIPFS"
      );
      const receipt1 = await tx1.wait();
      productId = receipt1.logs[0].args.productId;

      const tx2 = await marketplace.connect(seller).listProduct(productId);
      const receipt2 = await tx2.wait();
      listingId = receipt2.logs[0].args.listingId;
    });

    it("Should allow buyer to purchase product", async function () {
      const initialBuyerBalance = await usdcToken.balanceOf(buyer.address);
      const initialSellerBalance = await usdcToken.balanceOf(seller.address);
      const initialFeeBalance = await usdcToken.balanceOf(feeRecipient.address);

      await marketplace.connect(buyer).purchaseProduct(listingId);

      const finalBuyerBalance = await usdcToken.balanceOf(buyer.address);
      const finalSellerBalance = await usdcToken.balanceOf(seller.address);
      const finalFeeBalance = await usdcToken.balanceOf(feeRecipient.address);

      const expectedFee = (PRODUCT_PRICE * BigInt(MARKETPLACE_FEE_PERCENT)) / BigInt(10000);
      const expectedSellerAmount = PRODUCT_PRICE - expectedFee;

      expect(finalBuyerBalance).to.equal(initialBuyerBalance - PRODUCT_PRICE);
      expect(finalSellerBalance).to.equal(initialSellerBalance + expectedSellerAmount);
      expect(finalFeeBalance).to.equal(initialFeeBalance + expectedFee);
    });

    it("Should remove listing after purchase", async function () {
      await marketplace.connect(buyer).purchaseProduct(listingId);
      
      expect(await marketplace.isProductListed(productId)).to.be.false;
      expect(await marketplace.getActiveListingsCount()).to.equal(0);
    });

    it("Should record sale data correctly", async function () {
      await marketplace.connect(buyer).purchaseProduct(listingId);
      
      const buyerSales = await marketplace.getBuyerSales(buyer.address);
      expect(buyerSales.length).to.equal(1);
      
      const sale = buyerSales[0];
      expect(sale.buyer).to.equal(buyer.address);
      expect(sale.seller).to.equal(seller.address);
      expect(sale.priceUSDC).to.equal(PRODUCT_PRICE);
    });

    it("Should reject purchase from seller", async function () {
      await expect(
        marketplace.connect(seller).purchaseProduct(listingId)
      ).to.be.revertedWith("Cannot buy your own product");
    });

    it("Should reject purchase with insufficient USDC balance", async function () {
      // Transfer most USDC away from buyer
      await usdcToken.connect(buyer).transfer(owner.address, ethers.parseUnits("9950", USDC_DECIMALS));
      
      await expect(
        marketplace.connect(buyer).purchaseProduct(listingId)
      ).to.be.revertedWith("Insufficient USDC balance");
    });

    it("Should reject purchase with insufficient allowance", async function () {
      await usdcToken.connect(buyer).approve(await marketplace.getAddress(), 0);
      
      await expect(
        marketplace.connect(buyer).purchaseProduct(listingId)
      ).to.be.revertedWith("Insufficient USDC allowance");
    });
  });

  describe("View Functions", function () {
    let productListingId, productId;
    let product2Id, product2ListingId;

    beforeEach(async function () {
      // Create products in different categories
      const tx1 = await products.connect(seller).createProduct("Product 1", 1, PRODUCT_PRICE, "QmTest1");
      const receipt1 = await tx1.wait();
      productId = receipt1.logs[0].args.productId;
      
      const tx2 = await marketplace.connect(seller).listProduct(productId);
      const receipt2 = await tx2.wait();
      productListingId = receipt2.logs[0].args.listingId;

      // Create another category and product for testing category filtering
      await products.connect(seller).createCategory("Software", "Software products");
      
      const tx3 = await products.connect(seller).createProduct("Product 2", 2, PRODUCT_PRICE, "QmTest2");
      const receipt3 = await tx3.wait();
      product2Id = receipt3.logs[0].args.productId;
      
      const tx4 = await marketplace.connect(seller).listProduct(product2Id);
      const receipt4 = await tx4.wait();
      product2ListingId = receipt4.logs[0].args.listingId;
    });

    it("Should return all active listings", async function () {
      const listings = await marketplace.getAllActiveListings();
      expect(listings.length).to.equal(2);
    });

    it("Should return listings by category", async function () {
      const category1Listings = await marketplace.getActiveListingsByCategory(1); // Electronics category
      const category2Listings = await marketplace.getActiveListingsByCategory(2); // Software category
      
      expect(category1Listings.length).to.equal(1); // 1 product in category 1
      expect(category2Listings.length).to.equal(1); // 1 product in category 2
    });

    it("Should return empty array for non-existent category", async function () {
      const nonExistentCategoryListings = await marketplace.getActiveListingsByCategory(999);
      expect(nonExistentCategoryListings.length).to.equal(0);
    });

    it("Should return all categories from products contract", async function () {
      const categories = await marketplace.getAllCategories();
      expect(categories.length).to.equal(2); // Electronics and Software categories
      expect(categories[0].name).to.equal("Electronics");
      expect(categories[1].name).to.equal("Software");
    });

    it("Should return seller listings", async function () {
      const sellerListings = await marketplace.getSellerListings(seller.address);
      expect(sellerListings.length).to.equal(2);
    });

    it("Should return buyer sales after purchase", async function () {
      await marketplace.connect(buyer).purchaseProduct(productListingId);
      
      const buyerSales = await marketplace.getBuyerSales(buyer.address);
      expect(buyerSales.length).to.equal(1);
    });

    it("Should update category listings after purchase", async function () {
      // Check initial state
      const initialCategory1Listings = await marketplace.getActiveListingsByCategory(1);
      expect(initialCategory1Listings.length).to.equal(1);
      
      // Purchase a product from category 1
      await marketplace.connect(buyer).purchaseProduct(productListingId);
      
      // Check updated state
      const updatedCategory1Listings = await marketplace.getActiveListingsByCategory(1);
      expect(updatedCategory1Listings.length).to.equal(0); // Empty after purchase
    });
  });

  describe("Admin Functions", function () {
    it("Should allow owner to update marketplace fee", async function () {
      const newFee = 500; // 5%
      await marketplace.connect(owner).setMarketplaceFee(newFee);
      
      expect(await marketplace.marketplaceFeePercent()).to.equal(newFee);
    });

    it("Should reject fee update exceeding 10%", async function () {
      await expect(
        marketplace.connect(owner).setMarketplaceFee(1001) // 10.01%
      ).to.be.revertedWith("Fee cannot exceed 10%");
    });

    it("Should allow owner to update fee recipient", async function () {
      await marketplace.connect(owner).setFeeRecipient(admin.address);
      
      expect(await marketplace.feeRecipient()).to.equal(admin.address);
    });

    it("Should allow owner to pause/unpause marketplace", async function () {
      await marketplace.connect(owner).setMarketplaceStatus(false);
      expect(await marketplace.marketplaceActive()).to.be.false;
      
      await marketplace.connect(owner).setMarketplaceStatus(true);
      expect(await marketplace.marketplaceActive()).to.be.true;
    });

    it("Should reject listing when marketplace is paused", async function () {
      await marketplace.connect(owner).setMarketplaceStatus(false);
      
      const tx = await products.connect(seller).createProduct("Test", 1, PRODUCT_PRICE, "QmTest");
      const receipt = await tx.wait();
      const productId = receipt.logs[0].args.productId;
      
      await expect(
        marketplace.connect(seller).listProduct(productId)
      ).to.be.revertedWith("Marketplace is not active");
    });
  });

  describe("Emergency Functions", function () {
    let listingId, productId;

    beforeEach(async function () {
      const tx1 = await products.connect(seller).createProduct("Test", 1, PRODUCT_PRICE, "QmTest");
      const receipt1 = await tx1.wait();
      productId = receipt1.logs[0].args.productId;
      
      const tx2 = await marketplace.connect(seller).listProduct(productId);
      const receipt2 = await tx2.wait();
      listingId = receipt2.logs[0].args.listingId;
    });

    it("Should allow owner to emergency unlist", async function () {
      await marketplace.connect(owner).emergencyUnlistProduct(listingId);
      
      expect(await marketplace.isProductListed(productId)).to.be.false;
      expect(await marketplace.getActiveListingsCount()).to.equal(0);
    });

    it("Should reject emergency unlist from non-owner", async function () {
      await expect(
        marketplace.connect(seller).emergencyUnlistProduct(listingId)
      ).to.be.revertedWithCustomError(marketplace, "OwnableUnauthorizedAccount");
    });
  });
});