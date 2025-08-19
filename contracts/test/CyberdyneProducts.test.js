import { expect } from "chai";
import hre from "hardhat";
const { ethers } = hre;

describe("CyberdyneProducts", function () {
  let CyberdyneProducts;
  let cyberdyneProducts;
  let owner;
  let creator1;
  let creator2;
  let unauthorized;

  beforeEach(async function () {
    // Get signers
    [owner, creator1, creator2, unauthorized] = await ethers.getSigners();

    // Deploy the contract
    CyberdyneProducts = await ethers.getContractFactory("CyberdyneProducts");
    cyberdyneProducts = await CyberdyneProducts.deploy();
    await cyberdyneProducts.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await cyberdyneProducts.owner()).to.equal(owner.address);
    });

    it("Should initialize with zero products", async function () {
      expect(await cyberdyneProducts.totalProducts()).to.equal(0);
    });


    it("Should authorize owner as creator", async function () {
      expect(await cyberdyneProducts.isAuthorizedCreator(owner.address)).to.be.true;
    });
  });

  describe("Creator Authorization", function () {
    it("Should allow owner to authorize creators", async function () {
      await cyberdyneProducts.authorizeCreator(creator1.address);
      expect(await cyberdyneProducts.isAuthorizedCreator(creator1.address)).to.be.true;
    });

    it("Should emit CreatorAuthorized event", async function () {
      await expect(cyberdyneProducts.authorizeCreator(creator1.address))
        .to.emit(cyberdyneProducts, "CreatorAuthorized")
        .withArgs(creator1.address, owner.address);
    });

    it("Should not allow non-owner to authorize creators", async function () {
      await expect(
        cyberdyneProducts.connect(creator1).authorizeCreator(creator2.address)
      ).to.be.revertedWithCustomError(cyberdyneProducts, "OwnableUnauthorizedAccount");
    });

    it("Should not allow authorizing the same creator twice", async function () {
      await cyberdyneProducts.authorizeCreator(creator1.address);
      await expect(
        cyberdyneProducts.authorizeCreator(creator1.address)
      ).to.be.revertedWith("Creator already authorized");
    });

    it("Should allow owner to deauthorize creators", async function () {
      await cyberdyneProducts.authorizeCreator(creator1.address);
      await cyberdyneProducts.deauthorizeCreator(creator1.address);
      expect(await cyberdyneProducts.isAuthorizedCreator(creator1.address)).to.be.false;
    });

    it("Should not allow deauthorizing the owner", async function () {
      await expect(
        cyberdyneProducts.deauthorizeCreator(owner.address)
      ).to.be.revertedWith("Cannot deauthorize contract owner");
    });
  });

  describe("Product Creation", function () {
    beforeEach(async function () {
      await cyberdyneProducts.authorizeCreator(creator1.address);
    });

    it("Should allow authorized creators to create products", async function () {
      const tx = await cyberdyneProducts.connect(creator1).createProduct(
        "Trade4Me Pro",
        ethers.parseUnits("99.99", 6),
        "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
      );

      const receipt = await tx.wait();
      const event = receipt.logs.find(log => log.eventName === "ProductCreated");
      
      expect(event.args.title).to.equal("Trade4Me Pro");
      expect(event.args.priceUSDC).to.equal(ethers.parseUnits("99.99", 6));
      expect(event.args.creator).to.equal(creator1.address);
    });

    it("Should not allow unauthorized creators to create products", async function () {
      await expect(
        cyberdyneProducts.connect(unauthorized).createProduct(
          "Unauthorized Product",
          ethers.parseUnits("50.00", 6),
          "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
        )
      ).to.be.revertedWith("Not authorized to create products");
    });


    it("Should not allow empty title", async function () {
      await expect(
        cyberdyneProducts.connect(creator1).createProduct(
          "",
          ethers.parseUnits("50.00", 6),
          "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
        )
      ).to.be.revertedWith("Title cannot be empty");
    });

    it("Should not allow zero price", async function () {
      await expect(
        cyberdyneProducts.connect(creator1).createProduct(
          "Free Product",
          0,
          "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
        )
      ).to.be.revertedWith("Price must be greater than 0");
    });

    it("Should increment total products", async function () {
      await cyberdyneProducts.connect(creator1).createProduct(
        "Product 1",
        ethers.parseUnits("50.00", 6),
        "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
      );

      expect(await cyberdyneProducts.totalProducts()).to.equal(1);
    });
  });

  describe("Product Management", function () {
    let productUuid;

    beforeEach(async function () {
      await cyberdyneProducts.authorizeCreator(creator1.address);
      
      const tx = await cyberdyneProducts.connect(creator1).createProduct(
        "Test Product",
        ethers.parseUnits("99.99", 6),
        "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
      );

      const receipt = await tx.wait();
      const event = receipt.logs.find(log => log.eventName === "ProductCreated");
      productUuid = event.args.uuid;
    });

    it("Should allow creator to update product", async function () {
      await cyberdyneProducts.connect(creator1).updateProduct(
        productUuid,
        "Updated Product",
        ethers.parseUnits("149.99", 6),
        "QmNewIPFSHash"
      );

      const product = await cyberdyneProducts.getProduct(productUuid);
      expect(product.title).to.equal("Updated Product");
      expect(product.priceUSDC).to.equal(ethers.parseUnits("149.99", 6));
      expect(product.ipfsLocation).to.equal("QmNewIPFSHash");
    });

    it("Should allow owner to update any product", async function () {
      await cyberdyneProducts.connect(owner).updateProduct(
        productUuid,
        "Owner Updated",
        ethers.parseUnits("199.99", 6),
        "QmOwnerIPFSHash"
      );

      const product = await cyberdyneProducts.getProduct(productUuid);
      expect(product.title).to.equal("Owner Updated");
    });

    it("Should not allow unauthorized users to update product", async function () {
      await expect(
        cyberdyneProducts.connect(unauthorized).updateProduct(
          productUuid,
          "Unauthorized Update",
          ethers.parseUnits("199.99", 6),
          "QmUnauthorizedHash"
        )
      ).to.be.revertedWith("Only owner or creator can modify this product");
    });

    it("Should allow toggling product status", async function () {
      // Product should be active by default
      let product = await cyberdyneProducts.getProduct(productUuid);
      expect(product.isActive).to.be.true;

      // Toggle to inactive
      await cyberdyneProducts.connect(creator1).toggleProductStatus(productUuid);
      product = await cyberdyneProducts.getProduct(productUuid);
      expect(product.isActive).to.be.false;

      // Toggle back to active
      await cyberdyneProducts.connect(creator1).toggleProductStatus(productUuid);
      product = await cyberdyneProducts.getProduct(productUuid);
      expect(product.isActive).to.be.true;
    });

    it("Should allow deleting product", async function () {
      await cyberdyneProducts.connect(creator1).deleteProduct(productUuid);
      
      await expect(
        cyberdyneProducts.getProduct(productUuid)
      ).to.be.revertedWith("Product does not exist");

      expect(await cyberdyneProducts.totalProducts()).to.equal(0);
    });
  });

  describe("Product Queries", function () {
    beforeEach(async function () {
      await cyberdyneProducts.authorizeCreator(creator1.address);
      await cyberdyneProducts.authorizeCreator(creator2.address);

      // Create different products
      await cyberdyneProducts.connect(creator1).createProduct(
        "Product Pro",
        ethers.parseUnits("99.99", 6),
        "QmHash1"
      );

      await cyberdyneProducts.connect(creator1).createProduct(
        "Product Premium",
        ethers.parseUnits("149.99", 6),
        "QmHash2"
      );

      await cyberdyneProducts.connect(creator2).createProduct(
        "Product Basic",
        ethers.parseUnits("49.99", 6),
        "QmHash3"
      );
    });


    it("Should return products by creator", async function () {
      const creator1Products = await cyberdyneProducts.getProductsByCreator(creator1.address);
      expect(creator1Products.length).to.equal(2);

      const creator2Products = await cyberdyneProducts.getProductsByCreator(creator2.address);
      expect(creator2Products.length).to.equal(1);
    });

    it("Should return all products", async function () {
      const allProducts = await cyberdyneProducts.getAllProducts();
      expect(allProducts.length).to.equal(3);
    });

    it("Should return active products only", async function () {
      const allProducts = await cyberdyneProducts.getAllProducts();
      const firstProductUuid = allProducts[0].uuid;
      
      // Deactivate one product
      await cyberdyneProducts.connect(creator1).toggleProductStatus(firstProductUuid);
      
      const activeProducts = await cyberdyneProducts.getActiveProducts();
      expect(activeProducts.length).to.equal(2);
    });

    it("Should return correct counts", async function () {
      expect(await cyberdyneProducts.getCreatorProductCount(creator1.address)).to.equal(2);
      expect(await cyberdyneProducts.getCreatorProductCount(creator2.address)).to.equal(1);
      expect(await cyberdyneProducts.getActiveProductCount()).to.equal(3);
    });
  });

  describe("Contract Ownership", function () {
    it("Should transfer ownership correctly", async function () {
      await cyberdyneProducts.transferContractOwnership(creator1.address);
      
      expect(await cyberdyneProducts.owner()).to.equal(creator1.address);
      expect(await cyberdyneProducts.isAuthorizedCreator(creator1.address)).to.be.true;
    });

    it("Should not allow transferring to same owner", async function () {
      await expect(
        cyberdyneProducts.transferContractOwnership(owner.address)
      ).to.be.revertedWith("New owner cannot be the same as current owner");
    });

    it("Should not allow transferring to zero address", async function () {
      await expect(
        cyberdyneProducts.transferContractOwnership(ethers.ZeroAddress)
      ).to.be.revertedWith("New owner cannot be zero address");
    });
  });

  describe("Edge Cases", function () {
    beforeEach(async function () {
      await cyberdyneProducts.authorizeCreator(creator1.address);
    });

    it("Should handle non-existent product queries", async function () {
      await expect(
        cyberdyneProducts.getProduct("non-existent-uuid")
      ).to.be.revertedWith("Product does not exist");

      expect(await cyberdyneProducts.productExists("non-existent-uuid")).to.be.false;
    });

    it("Should handle empty product arrays", async function () {
      const unauthorizedProducts = await cyberdyneProducts.getProductsByCreator(unauthorized.address);
      expect(unauthorizedProducts.length).to.equal(0);
    });

    it("Should generate unique UUIDs", async function () {
      const tx1 = await cyberdyneProducts.connect(creator1).createProduct(
        "Product 1",
        ethers.parseUnits("50.00", 6),
        "QmHash1"
      );

      const tx2 = await cyberdyneProducts.connect(creator1).createProduct(
        "Product 2",
        ethers.parseUnits("60.00", 6),
        "QmHash2"
      );

      const receipt1 = await tx1.wait();
      const receipt2 = await tx2.wait();
      
      const event1 = receipt1.logs.find(log => log.eventName === "ProductCreated");
      const event2 = receipt2.logs.find(log => log.eventName === "ProductCreated");

      expect(event1.args.uuid).to.not.equal(event2.args.uuid);
    });
  });
});