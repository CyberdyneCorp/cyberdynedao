import { expect } from "chai";
import hre from "hardhat";
const { ethers } = hre;

describe("Deauthorization Semantics Tests", function () {
  let CyberdyneProducts;
  let products;
  let owner, creator1, creator2;
  let productUuid;

  beforeEach(async function () {
    [owner, creator1, creator2] = await ethers.getSigners();

    // Deploy CyberdyneProducts
    CyberdyneProducts = await ethers.getContractFactory("CyberdyneProducts");
    products = await CyberdyneProducts.deploy();
    await products.waitForDeployment();

    // Authorize creators and create category
    await products.authorizeCreator(creator1.address);
    await products.authorizeCreator(creator2.address);
    await products.connect(creator1).createCategory("Test", "Test category");

    // Create a product with creator1
    const tx = await products.connect(creator1).createProduct(
      "Test Product",
      1,
      ethers.parseUnits("100", 6),
      "QmTestIPFS"
    );
    const receipt = await tx.wait();
    productUuid = receipt.logs[0].args.uuid;
  });

  it("Should allow authorized creator to modify their own product", async function () {
    // Creator1 should be able to update their product
    await products.connect(creator1).updateProduct(
      productUuid,
      "Updated Product",
      1,
      ethers.parseUnits("150", 6),
      "QmUpdatedIPFS"
    );

    const product = await products.getProduct(productUuid);
    expect(product.title).to.equal("Updated Product");
    expect(product.priceUSDC).to.equal(ethers.parseUnits("150", 6));
  });

  it("Should prevent deauthorized creator from modifying their product", async function () {
    // Deauthorize creator1
    await products.deauthorizeCreator(creator1.address);

    // Creator1 should no longer be able to update their product
    await expect(
      products.connect(creator1).updateProduct(
        productUuid,
        "Should Fail Update",
        1,
        ethers.parseUnits("200", 6),
        "QmFailIPFS"
      )
    ).to.be.revertedWith("Only owner or authorized creator can modify this product");

    // Creator1 should no longer be able to toggle product status
    await expect(
      products.connect(creator1).toggleProductStatus(productUuid)
    ).to.be.revertedWith("Only owner or authorized creator can modify this product");

    // Creator1 should no longer be able to delete their product
    await expect(
      products.connect(creator1).deleteProduct(productUuid)
    ).to.be.revertedWith("Only owner or authorized creator can modify this product");
  });

  it("Should prevent other creators from modifying products they didn't create", async function () {
    // Creator2 should not be able to modify creator1's product
    await expect(
      products.connect(creator2).updateProduct(
        productUuid,
        "Unauthorized Update",
        1,
        ethers.parseUnits("300", 6),
        "QmUnauthorizedIPFS"
      )
    ).to.be.revertedWith("Only owner or authorized creator can modify this product");
  });

  it("Should always allow owner to modify any product regardless of creator authorization", async function () {
    // Deauthorize creator1
    await products.deauthorizeCreator(creator1.address);

    // Owner should still be able to modify the product
    await products.connect(owner).updateProduct(
      productUuid,
      "Owner Updated Product",
      1,
      ethers.parseUnits("250", 6),
      "QmOwnerIPFS"
    );

    const product = await products.getProduct(productUuid);
    expect(product.title).to.equal("Owner Updated Product");
    expect(product.priceUSDC).to.equal(ethers.parseUnits("250", 6));
  });

  it("Should prevent deauthorized creator from creating new products", async function () {
    // Deauthorize creator1
    await products.deauthorizeCreator(creator1.address);

    // Creator1 should not be able to create new products
    await expect(
      products.connect(creator1).createProduct(
        "New Product",
        1,
        ethers.parseUnits("100", 6),
        "QmNewIPFS"
      )
    ).to.be.revertedWith("Not authorized to create products");
  });

  it("Should allow re-authorized creator to regain product access", async function () {
    // Deauthorize creator1
    await products.deauthorizeCreator(creator1.address);

    // Verify they can't modify
    await expect(
      products.connect(creator1).updateProduct(
        productUuid,
        "Should Fail",
        1,
        ethers.parseUnits("200", 6),
        "QmFailIPFS"
      )
    ).to.be.revertedWith("Only owner or authorized creator can modify this product");

    // Re-authorize creator1
    await products.authorizeCreator(creator1.address);

    // Now they should be able to modify their product again
    await products.connect(creator1).updateProduct(
      productUuid,
      "Re-authorized Update",
      1,
      ethers.parseUnits("300", 6),
      "QmReauthIPFS"
    );

    const product = await products.getProduct(productUuid);
    expect(product.title).to.equal("Re-authorized Update");
  });
});