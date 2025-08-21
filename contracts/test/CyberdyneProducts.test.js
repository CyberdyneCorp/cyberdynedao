import { expect } from "chai";
import hre from "hardhat";
const { ethers } = hre;

// Helper function to convert bytes32 to string
function bytes32ToString(bytes32) {
  return ethers.decodeBytes32String(bytes32);
}

describe("CyberdyneProducts", function () {
  let CyberdyneProducts;
  let cyberdyneProducts;
  let owner;
  let creator1;
  let creator2;
  let unauthorized;
  let defaultCategoryId;
  let secondCategoryId;

  beforeEach(async function () {
    // Get signers
    [owner, creator1, creator2, unauthorized] = await ethers.getSigners();

    // Deploy the contract
    CyberdyneProducts = await ethers.getContractFactory("CyberdyneProducts");
    cyberdyneProducts = await CyberdyneProducts.deploy();
    await cyberdyneProducts.waitForDeployment();
    
    // Create a default category for testing
    const tx = await cyberdyneProducts.createCategory("Default Category", "Default category for testing");
    const receipt = await tx.wait();
    const event = receipt.logs.find(log => log.eventName === "CategoryCreated");
    defaultCategoryId = event.args.categoryId;
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await cyberdyneProducts.owner()).to.equal(owner.address);
    });

    it("Should initialize with zero products", async function () {
      expect(await cyberdyneProducts.getTotalProductCount()).to.equal(0);
    });

    it("Should initialize with nextCategoryId as 1", async function () {
      expect(await cyberdyneProducts.nextCategoryId()).to.be.greaterThan(1);
    });


    it("Should authorize owner as creator", async function () {
      expect(await cyberdyneProducts.isAuthorizedCreator(owner.address)).to.be.true;
    });
  });

  describe("Category Management", function () {
    it("Should allow authorized creators to create categories", async function () {
      await cyberdyneProducts.authorizeCreator(creator1.address);
      
      const tx = await cyberdyneProducts.connect(creator1).createCategory(
        "Software Tools",
        "Various software development tools"
      );
      
      const receipt = await tx.wait();
      const event = receipt.logs.find(log => log.eventName === "CategoryCreated");
      
      expect(event.args.name).to.equal("Software Tools");
      expect(event.args.categoryId).to.be.greaterThan(0);
    });

    it("Should not allow unauthorized creators to create categories", async function () {
      await expect(
        cyberdyneProducts.connect(unauthorized).createCategory(
          "Unauthorized Category",
          "This should fail"
        )
      ).to.be.revertedWith("Not authorized to create products");
    });

    it("Should not allow empty category name", async function () {
      await expect(
        cyberdyneProducts.createCategory("", "Empty name test")
      ).to.be.revertedWith("Category name cannot be empty");
    });

    it("Should return category information", async function () {
      const category = await cyberdyneProducts.getCategory(defaultCategoryId);
      expect(bytes32ToString(category.name)).to.equal("Default Category");
      expect(category.description).to.equal("Default category for testing");
      expect(category.exists).to.be.true;
    });

    it("Should return all categories", async function () {
      await cyberdyneProducts.createCategory("Test Category 2", "Second test category");
      
      const categories = await cyberdyneProducts.getAllCategories();
      expect(categories.length).to.be.greaterThanOrEqual(2);
    });

    it("Should check if category exists", async function () {
      expect(await cyberdyneProducts.categoryExists(defaultCategoryId)).to.be.true;
      expect(await cyberdyneProducts.categoryExists(999)).to.be.false;
    });

    it("Should not allow getting non-existent category", async function () {
      await expect(
        cyberdyneProducts.getCategory(999)
      ).to.be.revertedWith("Category does not exist");
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
        defaultCategoryId,
        ethers.parseUnits("99.99", 6),
        "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
      );

      const receipt = await tx.wait();
      const event = receipt.logs.find(log => log.eventName === "ProductCreated");
      
      expect(event.args.title).to.equal("Trade4Me Pro");
      expect(event.args.categoryId).to.equal(defaultCategoryId);
      expect(event.args.priceUSDC).to.equal(ethers.parseUnits("99.99", 6));
      expect(event.args.creator).to.equal(creator1.address);
    });

    it("Should not allow unauthorized creators to create products", async function () {
      await expect(
        cyberdyneProducts.connect(unauthorized).createProduct(
          "Unauthorized Product",
          defaultCategoryId,
          ethers.parseUnits("50.00", 6),
          "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
        )
      ).to.be.revertedWith("Not authorized to create products");
    });


    it("Should not allow empty title", async function () {
      await expect(
        cyberdyneProducts.connect(creator1).createProduct(
          "",
          defaultCategoryId,
          ethers.parseUnits("50.00", 6),
          "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
        )
      ).to.be.revertedWith("Title cannot be empty");
    });

    it("Should not allow zero price", async function () {
      await expect(
        cyberdyneProducts.connect(creator1).createProduct(
          "Free Product",
          defaultCategoryId,
          0,
          "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
        )
      ).to.be.revertedWith("Price must be greater than 0");
    });

    it("Should increment total products", async function () {
      await cyberdyneProducts.connect(creator1).createProduct(
        "Product 1",
        defaultCategoryId,
        ethers.parseUnits("50.00", 6),
        "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
      );

      expect(await cyberdyneProducts.getTotalProductCount()).to.equal(1);
    });

    it("Should not allow creating product with invalid category", async function () {
      await expect(
        cyberdyneProducts.connect(creator1).createProduct(
          "Invalid Category Product",
          999, // Invalid category ID
          ethers.parseUnits("50.00", 6),
          "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
        )
      ).to.be.revertedWith("Category does not exist");
    });
  });

  describe("Product Management", function () {
    let productId;

    beforeEach(async function () {
      await cyberdyneProducts.authorizeCreator(creator1.address);
      
      const tx = await cyberdyneProducts.connect(creator1).createProduct(
        "Test Product",
        defaultCategoryId,
        ethers.parseUnits("99.99", 6),
        "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA"
      );

      const receipt = await tx.wait();
      const event = receipt.logs.find(log => log.eventName === "ProductCreated");
      productId = event.args.productId;
    });

    it("Should allow creator to update product", async function () {
      await cyberdyneProducts.connect(creator1).updateProduct(
        productId,
        "Updated Product",
        defaultCategoryId,
        ethers.parseUnits("149.99", 6),
        "QmNewIPFSHash"
      );

      const product = await cyberdyneProducts.getProduct(productId);
      expect(bytes32ToString(product.title)).to.equal("Updated Product");
      expect(product.categoryId).to.equal(defaultCategoryId);
      expect(product.priceUSDC).to.equal(ethers.parseUnits("149.99", 6));
      expect(product.metadataURI).to.equal("QmNewIPFSHash");
    });

    it("Should allow owner to update any product", async function () {
      await cyberdyneProducts.connect(owner).updateProduct(
        productId,
        "Owner Updated",
        defaultCategoryId,
        ethers.parseUnits("199.99", 6),
        "QmOwnerIPFSHash"
      );

      const product = await cyberdyneProducts.getProduct(productId);
      expect(bytes32ToString(product.title)).to.equal("Owner Updated");
    });

    it("Should not allow unauthorized users to update product", async function () {
      await expect(
        cyberdyneProducts.connect(unauthorized).updateProduct(
          productId,
          "Unauthorized Update",
          defaultCategoryId,
          ethers.parseUnits("199.99", 6),
          "QmUnauthorizedHash"
        )
      ).to.be.revertedWith("Only owner or authorized creator can modify this product");
    });

    it("Should allow toggling product status", async function () {
      // Product should be active by default
      let product = await cyberdyneProducts.getProduct(productId);
      expect(product.isActive).to.be.true;

      // Toggle to inactive
      await cyberdyneProducts.connect(creator1).toggleProductStatus(productId);
      product = await cyberdyneProducts.getProduct(productId);
      expect(product.isActive).to.be.false;

      // Toggle back to active
      await cyberdyneProducts.connect(creator1).toggleProductStatus(productId);
      product = await cyberdyneProducts.getProduct(productId);
      expect(product.isActive).to.be.true;
    });

    it("Should allow updating product category", async function () {
      // Create a second category first
      const tx = await cyberdyneProducts.createCategory("New Category", "Updated category");
      const receipt = await tx.wait();
      const event = receipt.logs.find(log => log.eventName === "CategoryCreated");
      const newCategoryId = event.args.categoryId;

      // Update product to new category
      await cyberdyneProducts.connect(creator1).updateProduct(
        productId,
        "Updated Product",
        newCategoryId,
        ethers.parseUnits("149.99", 6),
        "QmNewIPFSHash"
      );

      const product = await cyberdyneProducts.getProduct(productId);
      expect(product.categoryId).to.equal(newCategoryId);

      // Verify product moved from default category to new category
      const defaultCategoryProducts = await cyberdyneProducts.getAllProductsByCategory(defaultCategoryId);
      expect(defaultCategoryProducts.length).to.equal(0);

      const newCategoryProducts = await cyberdyneProducts.getAllProductsByCategory(newCategoryId);
      expect(newCategoryProducts.length).to.equal(1);
      expect(newCategoryProducts[0].id).to.equal(productId);
    });

    it("Should allow deleting product", async function () {
      await cyberdyneProducts.connect(creator1).deleteProduct(productId);
      
      await expect(
        cyberdyneProducts.getProduct(productId)
      ).to.be.revertedWith("Product does not exist");

      expect(await cyberdyneProducts.getTotalProductCount()).to.equal(0);
    });
  });

  describe("Product Queries", function () {
    let secondCategoryId;
    
    beforeEach(async function () {
      await cyberdyneProducts.authorizeCreator(creator1.address);
      await cyberdyneProducts.authorizeCreator(creator2.address);

      // Create a second category
      const tx = await cyberdyneProducts.createCategory("Premium Tools", "Premium software tools");
      const receipt = await tx.wait();
      const event = receipt.logs.find(log => log.eventName === "CategoryCreated");
      secondCategoryId = event.args.categoryId;

      // Create different products in different categories
      await cyberdyneProducts.connect(creator1).createProduct(
        "Product Pro",
        defaultCategoryId,
        ethers.parseUnits("99.99", 6),
        "QmHash1"
      );

      await cyberdyneProducts.connect(creator1).createProduct(
        "Product Premium",
        secondCategoryId,
        ethers.parseUnits("149.99", 6),
        "QmHash2"
      );

      await cyberdyneProducts.connect(creator2).createProduct(
        "Product Basic",
        defaultCategoryId,
        ethers.parseUnits("49.99", 6),
        "QmHash3"
      );
    });


    it("Should return products by creator", async function () {
      const creator1Products = await cyberdyneProducts.getAllProductsByCreator(creator1.address);
      expect(creator1Products.length).to.equal(2);

      const creator2Products = await cyberdyneProducts.getAllProductsByCreator(creator2.address);
      expect(creator2Products.length).to.equal(1);
    });

    it("Should return all products", async function () {
      const allProducts = await cyberdyneProducts.getAllProducts();
      expect(allProducts.length).to.equal(3);
    });

    it("Should return active products only", async function () {
      const allProducts = await cyberdyneProducts.getAllProducts();
      const firstProductId = allProducts[0].id;
      
      // Deactivate one product
      await cyberdyneProducts.connect(creator1).toggleProductStatus(firstProductId);
      
      const activeProducts = await cyberdyneProducts.getAllActiveProducts();
      expect(activeProducts.length).to.equal(2);
    });

    it("Should return products by category", async function () {
      const defaultCategoryProducts = await cyberdyneProducts.getAllProductsByCategory(defaultCategoryId);
      expect(defaultCategoryProducts.length).to.equal(2);
      
      const premiumCategoryProducts = await cyberdyneProducts.getAllProductsByCategory(secondCategoryId);
      expect(premiumCategoryProducts.length).to.equal(1);
      expect(bytes32ToString(premiumCategoryProducts[0].title)).to.equal("Product Premium");
    });

    it("Should return category product count", async function () {
      expect(await cyberdyneProducts.getCategoryProductCount(defaultCategoryId)).to.equal(2);
      expect(await cyberdyneProducts.getCategoryProductCount(secondCategoryId)).to.equal(1);
    });

    it("Should not allow querying invalid category", async function () {
      await expect(
        cyberdyneProducts.getAllProductsByCategory(999)
      ).to.be.revertedWith("Category does not exist");
      
      await expect(
        cyberdyneProducts.getCategoryProductCount(999)
      ).to.be.revertedWith("Category does not exist");
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
        cyberdyneProducts.getProduct(999)
      ).to.be.revertedWith("Product does not exist");

      expect(await cyberdyneProducts.productExists(999)).to.be.false;
    });

    it("Should handle empty product arrays", async function () {
      const unauthorizedProducts = await cyberdyneProducts.getAllProductsByCreator(unauthorized.address);
      expect(unauthorizedProducts.length).to.equal(0);
    });

    it("Should generate unique IDs", async function () {
      const tx1 = await cyberdyneProducts.connect(creator1).createProduct(
        "Product 1",
        defaultCategoryId,
        ethers.parseUnits("50.00", 6),
        "QmHash1"
      );

      const tx2 = await cyberdyneProducts.connect(creator1).createProduct(
        "Product 2",
        defaultCategoryId,
        ethers.parseUnits("60.00", 6),
        "QmHash2"
      );

      const receipt1 = await tx1.wait();
      const receipt2 = await tx2.wait();
      
      const event1 = receipt1.logs.find(log => log.eventName === "ProductCreated");
      const event2 = receipt2.logs.find(log => log.eventName === "ProductCreated");

      expect(event1.args.productId).to.not.equal(event2.args.productId);
    });
  });
});