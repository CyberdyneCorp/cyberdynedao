import { expect } from "chai";
import hre from "hardhat";
const { ethers } = hre;

describe("Ownership Authorization Bug Fix", function () {
  let CyberdyneProducts;
  let products;
  let owner, newOwner, creator1;

  beforeEach(async function () {
    [owner, newOwner, creator1] = await ethers.getSigners();

    // Deploy CyberdyneProducts
    CyberdyneProducts = await ethers.getContractFactory("CyberdyneProducts");
    products = await CyberdyneProducts.deploy();
    await products.waitForDeployment();

    // Add some authorized creators to ensure we have a non-trivial list
    await products.authorizeCreator(creator1.address);
  });

  it("Should correctly handle ownership transfer with O(1) authorization index", async function () {
    // Initial state: owner and creator1 are authorized
    let authorizedCreators = await products.getAuthorizedCreators();
    expect(authorizedCreators.length).to.equal(2);
    expect(authorizedCreators).to.include(owner.address);
    expect(authorizedCreators).to.include(creator1.address);

    // Transfer ownership to newOwner (who isn't currently authorized)
    await products.transferContractOwnership(newOwner.address);

    // Verify newOwner is now authorized and in the list
    authorizedCreators = await products.getAuthorizedCreators();
    expect(authorizedCreators.length).to.equal(3);
    expect(authorizedCreators).to.include(newOwner.address);
    expect(await products.isAuthorizedCreator(newOwner.address)).to.be.true;

    // Critical test: Try to deauthorize the new owner from someone else
    // This should work correctly without corrupting the list
    const anotherAddress = ethers.Wallet.createRandom().address;
    await products.connect(newOwner).authorizeCreator(anotherAddress);
    
    // Verify the new address is added correctly
    authorizedCreators = await products.getAuthorizedCreators();
    expect(authorizedCreators.length).to.equal(4);
    expect(authorizedCreators).to.include(anotherAddress);

    // Now deauthorize the new creator - this should not corrupt the list
    await products.connect(newOwner).deauthorizeCreator(anotherAddress);
    
    // Verify the list is still intact and correctly sized
    authorizedCreators = await products.getAuthorizedCreators();
    expect(authorizedCreators.length).to.equal(3);
    expect(authorizedCreators).to.not.include(anotherAddress);
    
    // All original addresses should still be present
    expect(authorizedCreators).to.include(owner.address);
    expect(authorizedCreators).to.include(creator1.address);
    expect(authorizedCreators).to.include(newOwner.address);
  });

  it("Should not affect ownership transfer when new owner is already authorized", async function () {
    // First authorize the newOwner
    await products.authorizeCreator(newOwner.address);
    
    // Initial state: 3 authorized creators
    let authorizedCreators = await products.getAuthorizedCreators();
    expect(authorizedCreators.length).to.equal(3);

    // Transfer ownership to already-authorized newOwner
    await products.transferContractOwnership(newOwner.address);

    // List should remain the same size (no duplicate addition)
    authorizedCreators = await products.getAuthorizedCreators();
    expect(authorizedCreators.length).to.equal(3);
    expect(authorizedCreators).to.include(newOwner.address);
    
    // Should still be able to deauthorize other creators correctly
    await products.connect(newOwner).deauthorizeCreator(creator1.address);
    
    authorizedCreators = await products.getAuthorizedCreators();
    expect(authorizedCreators.length).to.equal(2);
    expect(authorizedCreators).to.not.include(creator1.address);
    expect(authorizedCreators).to.include(owner.address);
    expect(authorizedCreators).to.include(newOwner.address);
  });

  it("Should correctly maintain index integrity after ownership transfer", async function () {
    // Add several creators to create a more complex scenario
    const additionalCreators = [];
    for (let i = 0; i < 5; i++) {
      const wallet = ethers.Wallet.createRandom();
      additionalCreators.push(wallet.address);
      await products.authorizeCreator(wallet.address);
    }

    // Now we have: owner, creator1, + 5 additional = 7 total
    let authorizedCreators = await products.getAuthorizedCreators();
    expect(authorizedCreators.length).to.equal(7);

    // Transfer ownership to newOwner (not previously authorized)
    await products.transferContractOwnership(newOwner.address);

    // Should now have 8 total
    authorizedCreators = await products.getAuthorizedCreators();
    expect(authorizedCreators.length).to.equal(8);

    // Test removing creators from various positions in the list
    // Remove first additional creator
    await products.connect(newOwner).deauthorizeCreator(additionalCreators[0]);
    expect((await products.getAuthorizedCreators()).length).to.equal(7);

    // Remove middle creator
    await products.connect(newOwner).deauthorizeCreator(additionalCreators[2]);
    expect((await products.getAuthorizedCreators()).length).to.equal(6);

    // Remove last additional creator
    await products.connect(newOwner).deauthorizeCreator(additionalCreators[4]);
    expect((await products.getAuthorizedCreators()).length).to.equal(5);

    // Verify all remaining expected addresses are still present
    const finalCreators = await products.getAuthorizedCreators();
    expect(finalCreators).to.include(owner.address);
    expect(finalCreators).to.include(creator1.address);
    expect(finalCreators).to.include(newOwner.address);
    expect(finalCreators).to.include(additionalCreators[1]);
    expect(finalCreators).to.include(additionalCreators[3]);
    
    // Verify removed addresses are not present
    expect(finalCreators).to.not.include(additionalCreators[0]);
    expect(finalCreators).to.not.include(additionalCreators[2]);
    expect(finalCreators).to.not.include(additionalCreators[4]);
  });
});