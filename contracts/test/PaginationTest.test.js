import { expect } from "chai";
import hre from "hardhat";
const { ethers } = hre;

// Helper function to convert bytes32 to string
function bytes32ToString(bytes32) {
  return ethers.decodeBytes32String(bytes32);
}

describe("Pagination Functions Tests", function () {
  let CyberdyneProducts;
  let products;
  let owner, creator;

  beforeEach(async function () {
    [owner, creator] = await ethers.getSigners();

    // Deploy CyberdyneProducts
    CyberdyneProducts = await ethers.getContractFactory("CyberdyneProducts");
    products = await CyberdyneProducts.deploy();
    await products.waitForDeployment();

    // Authorize creator and create category
    await products.authorizeCreator(creator.address);
    await products.connect(creator).createCategory("Test", "Test category");
  });

  it("Should return paginated products correctly", async function () {
    // Create 5 products
    const productIds = [];
    for (let i = 0; i < 5; i++) {
      const tx = await products.connect(creator).createProduct(
        `Product ${i}`,
        1,
        ethers.parseUnits("100", 6),
        `QmTestIPFS${i}`
      );
      const receipt = await tx.wait();
      productIds.push(receipt.logs[0].args.productId);
    }

    // Test pagination
    const page1 = await products.getProducts(0, 2); // First 2 products
    const page2 = await products.getProducts(2, 2); // Next 2 products  
    const page3 = await products.getProducts(4, 2); // Last 1 product

    expect(page1.length).to.equal(2);
    expect(page2.length).to.equal(2);
    expect(page3.length).to.equal(1);

    // Verify correct products are returned
    expect(page1[0].title).to.equal("Product 0");
    expect(page1[1].title).to.equal("Product 1");
    expect(page2[0].title).to.equal("Product 2");
    expect(page2[1].title).to.equal("Product 3");
    expect(page3[0].title).to.equal("Product 4");
  });

  it("Should handle out-of-bounds pagination gracefully", async function () {
    // Create 2 products
    for (let i = 0; i < 2; i++) {
      await products.connect(creator).createProduct(
        `Product ${i}`,
        1,
        ethers.parseUnits("100", 6),
        `QmTestIPFS${i}`
      );
    }

    // Test beyond bounds
    const emptyPage = await products.getProducts(10, 5);
    expect(emptyPage.length).to.equal(0);

    // Test partial page
    const partialPage = await products.getProducts(1, 5);
    expect(partialPage.length).to.equal(1); // Only 1 product left
  });

  it("Should return paginated products by creator", async function () {
    // Create 3 products with creator
    for (let i = 0; i < 3; i++) {
      await products.connect(creator).createProduct(
        `Creator Product ${i}`,
        1,
        ethers.parseUnits("100", 6),
        `QmTestIPFS${i}`
      );
    }

    const page1 = await products.getProductsByCreator(creator.address, 0, 2);
    const page2 = await products.getProductsByCreator(creator.address, 2, 2);

    expect(page1.length).to.equal(2);
    expect(page2.length).to.equal(1);
    expect(page1[0].creator).to.equal(creator.address);
    expect(page2[0].creator).to.equal(creator.address);
  });

  it("Should return paginated products by category", async function () {
    // Create second category
    await products.connect(creator).createCategory("Software", "Software category");
    
    // Create products in both categories
    await products.connect(creator).createProduct("Cat1 Product 1", 1, ethers.parseUnits("100", 6), "QmTest1");
    await products.connect(creator).createProduct("Cat1 Product 2", 1, ethers.parseUnits("100", 6), "QmTest2");
    await products.connect(creator).createProduct("Cat2 Product 1", 2, ethers.parseUnits("100", 6), "QmTest3");

    const cat1Page = await products.getProductsByCategory(1, 0, 1);
    const cat2Page = await products.getProductsByCategory(2, 0, 1);

    expect(cat1Page.length).to.equal(1);
    expect(cat2Page.length).to.equal(1);
    expect(cat1Page[0].categoryId).to.equal(1);
    expect(cat2Page[0].categoryId).to.equal(2);
  });

  it("Should return paginated active products only", async function () {
    // Create 3 products
    const productIds = [];
    for (let i = 0; i < 3; i++) {
      const tx = await products.connect(creator).createProduct(
        `Product ${i}`,
        1,
        ethers.parseUnits("100", 6),
        `QmTestIPFS${i}`
      );
      const receipt = await tx.wait();
      productIds.push(receipt.logs[0].args.productId);
    }

    // Deactivate middle product
    await products.connect(creator).toggleProductStatus(productIds[1]);

    const activePage = await products.getActiveProductsPaginated(0, 5);
    expect(activePage.length).to.equal(2); // Only 2 active products
    
    // Verify all returned products are active
    for (const product of activePage) {
      expect(product.isActive).to.be.true;
    }
  });
});