import { expect } from "chai";
import hre from "hardhat";
import { loadFixture } from "@nomicfoundation/hardhat-toolbox/network-helpers.js";
const { ethers } = hre;

// Helper function to convert bytes32 to string
function bytes32ToString(bytes32) {
  return ethers.decodeBytes32String(bytes32);
}

describe("TrainingMaterials", function () {
  // Test data
  const CATEGORY_NAME = "Blockchain Fundamentals";
  const CATEGORY_DESCRIPTION = "Learn the basics of blockchain technology";
  
  const MATERIAL_TITLE = "Introduction to Smart Contracts";
  const MATERIAL_DESCRIPTION = "A comprehensive guide to smart contracts";
  const MATERIAL_IMAGE_IPFS = "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG";
  const MATERIAL_CONTENT_IPFS = "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdH";
  const MATERIAL_CONTEXT_IPFS = "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdI";
  const MATERIAL_PRICE_USDC = ethers.parseUnits("29.99", 6); // 29.99 USDC (6 decimals)

  async function deployTrainingMaterialsFixture() {
    const [owner, otherAccount, authorizedCreator, newOwner] = await ethers.getSigners();
    const TrainingMaterials = await ethers.getContractFactory("TrainingMaterials");
    const contract = await TrainingMaterials.deploy();

    return { contract, owner, otherAccount, authorizedCreator, newOwner };
  }

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      const { contract, owner } = await loadFixture(deployTrainingMaterialsFixture);
      expect(await contract.owner()).to.equal(owner.address);
    });

    it("Should initialize with correct default values", async function () {
      const { contract, owner } = await loadFixture(deployTrainingMaterialsFixture);
      expect(await contract.nextCategoryId()).to.equal(1);
      expect(await contract.getTotalMaterialCount()).to.equal(0);
      
      // Owner should be automatically authorized
      expect(await contract.isAuthorizedCreator(owner.address)).to.be.true;
      expect(await contract.getAuthorizedCreatorsCount()).to.equal(1);
      
      const authorizedCreators = await contract.getAuthorizedCreators();
      expect(authorizedCreators).to.have.lengthOf(1);
      expect(authorizedCreators[0]).to.equal(owner.address);
    });
  });

  describe("Creator Authorization", function () {
    describe("Authorizing Creators", function () {
      it("Should allow owner to authorize new creators", async function () {
        const { contract, owner, authorizedCreator } = await loadFixture(deployTrainingMaterialsFixture);
        
        await expect(contract.authorizeCreator(authorizedCreator.address))
          .to.emit(contract, "CreatorAuthorized")
          .withArgs(authorizedCreator.address, owner.address);

        expect(await contract.isAuthorizedCreator(authorizedCreator.address)).to.be.true;
        expect(await contract.getAuthorizedCreatorsCount()).to.equal(2);
      });

      it("Should revert when non-owner tries to authorize creators", async function () {
        const { contract, otherAccount, authorizedCreator } = await loadFixture(deployTrainingMaterialsFixture);
        
        await expect(
          contract.connect(otherAccount).authorizeCreator(authorizedCreator.address)
        ).to.be.revertedWithCustomError(contract, "OwnableUnauthorizedAccount");
      });

      it("Should revert when trying to authorize zero address", async function () {
        const { contract } = await loadFixture(deployTrainingMaterialsFixture);
        
        await expect(
          contract.authorizeCreator(ethers.ZeroAddress)
        ).to.be.revertedWith("Cannot authorize zero address");
      });

      it("Should revert when trying to authorize already authorized creator", async function () {
        const { contract, authorizedCreator } = await loadFixture(deployTrainingMaterialsFixture);
        
        await contract.authorizeCreator(authorizedCreator.address);
        
        await expect(
          contract.authorizeCreator(authorizedCreator.address)
        ).to.be.revertedWith("Creator already authorized");
      });
    });

    describe("Deauthorizing Creators", function () {
      it("Should allow owner to deauthorize creators", async function () {
        const { contract, owner, authorizedCreator } = await loadFixture(deployTrainingMaterialsFixture);
        
        await contract.authorizeCreator(authorizedCreator.address);
        
        await expect(contract.deauthorizeCreator(authorizedCreator.address))
          .to.emit(contract, "CreatorDeauthorized")
          .withArgs(authorizedCreator.address, owner.address);

        expect(await contract.isAuthorizedCreator(authorizedCreator.address)).to.be.false;
        expect(await contract.getAuthorizedCreatorsCount()).to.equal(1); // Only owner remains
      });

      it("Should not allow deauthorizing the contract owner", async function () {
        const { contract, owner } = await loadFixture(deployTrainingMaterialsFixture);
        
        await expect(
          contract.deauthorizeCreator(owner.address)
        ).to.be.revertedWith("Cannot deauthorize contract owner");
      });

      it("Should revert when trying to deauthorize non-authorized creator", async function () {
        const { contract, otherAccount } = await loadFixture(deployTrainingMaterialsFixture);
        
        await expect(
          contract.deauthorizeCreator(otherAccount.address)
        ).to.be.revertedWith("Creator not authorized");
      });
    });

    describe("Creator Queries", function () {
      it("Should return correct authorized creators list", async function () {
        const { contract, owner, authorizedCreator, otherAccount } = await loadFixture(deployTrainingMaterialsFixture);
        
        await contract.authorizeCreator(authorizedCreator.address);
        await contract.authorizeCreator(otherAccount.address);
        
        const creators = await contract.getAuthorizedCreators();
        expect(creators).to.have.lengthOf(3);
        expect(creators).to.include(owner.address);
        expect(creators).to.include(authorizedCreator.address);
        expect(creators).to.include(otherAccount.address);
      });
    });
  });

  describe("Contract Ownership Transfer", function () {
    it("Should allow owner to transfer contract ownership", async function () {
      const { contract, owner, newOwner } = await loadFixture(deployTrainingMaterialsFixture);
      
      expect(await contract.owner()).to.equal(owner.address);
      expect(await contract.isAuthorizedCreator(newOwner.address)).to.be.false;
      
      await expect(contract.transferContractOwnership(newOwner.address))
        .to.emit(contract, "ContractOwnershipTransferred")
        .withArgs(owner.address, newOwner.address);
      
      // Verify ownership has transferred
      expect(await contract.owner()).to.equal(newOwner.address);
      
      // Verify new owner is automatically authorized
      expect(await contract.isAuthorizedCreator(newOwner.address)).to.be.true;
    });

    it("Should revert if non-owner tries to transfer ownership", async function () {
      const { contract, otherAccount, newOwner } = await loadFixture(deployTrainingMaterialsFixture);
      
      await expect(
        contract.connect(otherAccount).transferContractOwnership(newOwner.address)
      ).to.be.revertedWithCustomError(contract, "OwnableUnauthorizedAccount");
    });

    it("Should revert if trying to transfer to zero address", async function () {
      const { contract } = await loadFixture(deployTrainingMaterialsFixture);
      
      await expect(
        contract.transferContractOwnership(ethers.ZeroAddress)
      ).to.be.revertedWith("New owner cannot be zero address");
    });

    it("Should revert if trying to transfer to current owner", async function () {
      const { contract, owner } = await loadFixture(deployTrainingMaterialsFixture);
      
      await expect(
        contract.transferContractOwnership(owner.address)
      ).to.be.revertedWith("New owner cannot be the same as current owner");
    });

    it("Should maintain existing authorization if new owner is already authorized", async function () {
      const { contract, owner, newOwner } = await loadFixture(deployTrainingMaterialsFixture);
      
      // First authorize the new owner
      await contract.authorizeCreator(newOwner.address);
      const initialCount = await contract.getAuthorizedCreatorsCount();
      
      // Transfer ownership
      await contract.transferContractOwnership(newOwner.address);
      
      // Count should remain the same (no duplicate authorization)
      expect(await contract.getAuthorizedCreatorsCount()).to.equal(initialCount);
      expect(await contract.isAuthorizedCreator(newOwner.address)).to.be.true;
    });

    it("Should allow new owner to perform owner-only functions", async function () {
      const { contract, owner, newOwner, authorizedCreator } = await loadFixture(deployTrainingMaterialsFixture);
      
      // Transfer ownership
      await contract.transferContractOwnership(newOwner.address);
      
      // New owner should be able to create categories
      await expect(
        contract.connect(newOwner).createCategory("New Category", "Created by new owner")
      ).to.emit(contract, "CategoryCreated");
      
      // New owner should be able to authorize creators
      await expect(
        contract.connect(newOwner).authorizeCreator(authorizedCreator.address)
      ).to.emit(contract, "CreatorAuthorized");
      
      // Previous owner should no longer be able to perform owner functions
      await expect(
        contract.connect(owner).createCategory("Another Category", "Should fail")
      ).to.be.revertedWithCustomError(contract, "OwnableUnauthorizedAccount");
    });
  });

  describe("Category Management", function () {
    describe("Creating Categories", function () {
      it("Should allow owner to create a category", async function () {
        const { contract } = await loadFixture(deployTrainingMaterialsFixture);
        
        await expect(contract.createCategory(CATEGORY_NAME, CATEGORY_DESCRIPTION))
          .to.emit(contract, "CategoryCreated")
          .withArgs(1, CATEGORY_NAME, CATEGORY_DESCRIPTION);

        const category = await contract.getCategory(1);
        expect(category.id).to.equal(1);
        expect(bytes32ToString(category.name)).to.equal(CATEGORY_NAME);
        expect(category.description).to.equal(CATEGORY_DESCRIPTION);
        expect(category.exists).to.be.true;
      });

      it("Should increment category ID for each new category", async function () {
        const { contract } = await loadFixture(deployTrainingMaterialsFixture);
        
        await contract.createCategory("Category 1", "Description 1");
        await contract.createCategory("Category 2", "Description 2");

        expect(await contract.nextCategoryId()).to.equal(3);
      });

      it("Should revert if non-owner tries to create a category", async function () {
        const { contract, otherAccount } = await loadFixture(deployTrainingMaterialsFixture);
        
        await expect(
          contract.connect(otherAccount).createCategory(CATEGORY_NAME, CATEGORY_DESCRIPTION)
        ).to.be.revertedWithCustomError(contract, "OwnableUnauthorizedAccount");
      });

      it("Should revert if category name is empty", async function () {
        const { contract } = await loadFixture(deployTrainingMaterialsFixture);
        
        await expect(
          contract.createCategory("", CATEGORY_DESCRIPTION)
        ).to.be.revertedWith("Category name cannot be empty");
      });
    });

    describe("Category Queries", function () {
      it("Should return correct category information", async function () {
        const { contract } = await loadFixture(deployTrainingMaterialsFixture);
        
        await contract.createCategory(CATEGORY_NAME, CATEGORY_DESCRIPTION);
        
        const category = await contract.getCategory(1);
        expect(bytes32ToString(category.name)).to.equal(CATEGORY_NAME);
        expect(category.description).to.equal(CATEGORY_DESCRIPTION);
        expect(category.exists).to.be.true;
      });

      it("Should revert when querying non-existent category", async function () {
        const { contract } = await loadFixture(deployTrainingMaterialsFixture);
        
        await expect(
          contract.getCategory(999)
        ).to.be.revertedWith("Category does not exist");
      });

      it("Should return all categories", async function () {
        const { contract } = await loadFixture(deployTrainingMaterialsFixture);
        
        await contract.createCategory("Category 1", "Description 1");
        await contract.createCategory("Category 2", "Description 2");
        await contract.createCategory("Category 3", "Description 3");

        const categories = await contract.getAllCategories();
        expect(categories.length).to.equal(3);
        expect(categories[0].name).to.equal("Category 1");
        expect(categories[1].name).to.equal("Category 2");
        expect(categories[2].name).to.equal("Category 3");
      });

      it("Should check if category exists", async function () {
        const { contract } = await loadFixture(deployTrainingMaterialsFixture);
        
        await contract.createCategory(CATEGORY_NAME, CATEGORY_DESCRIPTION);
        
        expect(await contract.categoryExists(1)).to.be.true;
        expect(await contract.categoryExists(999)).to.be.false;
      });
    });
  });

  describe("Training Material Management", function () {
    async function deployWithCategoryFixture() {
      const fixture = await deployTrainingMaterialsFixture();
      await fixture.contract.createCategory(CATEGORY_NAME, CATEGORY_DESCRIPTION);
      return fixture;
    }

    describe("Creating Training Materials", function () {
      it("Should allow owner to create a training material", async function () {
        const { contract, owner } = await loadFixture(deployWithCategoryFixture);
        
        const tx = await contract.createTrainingMaterial(
          MATERIAL_TITLE,
          1,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_PRICE_USDC
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const generatedMaterialId = event.args.materialId;
        
        expect(generatedMaterialId).to.be.a('bigint');
        expect(generatedMaterialId).to.be.greaterThan(0);

        const material = await contract.getTrainingMaterial(generatedMaterialId);
        expect(material.id).to.equal(generatedMaterialId);
        expect(bytes32ToString(material.title)).to.equal(MATERIAL_TITLE);
        expect(material.categoryId).to.equal(1);
        expect(material.metadataURI).to.equal(MATERIAL_CONTENT_IPFS);
        expect(material.priceUSDC).to.equal(MATERIAL_PRICE_USDC);
        expect(material.creator).to.equal(owner.address);
        expect(material.exists).to.be.true;
      });

      it("Should increment total materials count", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        expect(await contract.getTotalMaterialCount()).to.equal(0);
        
        await contract.createTrainingMaterial(
          MATERIAL_TITLE,
          1,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_PRICE_USDC
        );

        expect(await contract.getTotalMaterialCount()).to.equal(1);
      });

      it("Should revert if non-authorized user tries to create training material", async function () {
        const { contract, otherAccount } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.connect(otherAccount).createTrainingMaterial(
            MATERIAL_TITLE,
            1,
            MATERIAL_CONTENT_IPFS,
            MATERIAL_PRICE_USDC
          )
        ).to.be.revertedWith("Not authorized to create training materials");
      });

      it("Should allow authorized creator to create training material", async function () {
        const { contract, owner, authorizedCreator } = await loadFixture(deployWithCategoryFixture);
        
        // Authorize the creator
        await contract.authorizeCreator(authorizedCreator.address);
        
        const tx = await contract.connect(authorizedCreator).createTrainingMaterial(
          MATERIAL_TITLE,
          1,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_PRICE_USDC
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const generatedMaterialId = event.args.materialId;
        
        const material = await contract.getTrainingMaterial(generatedMaterialId);
        expect(material.creator).to.equal(authorizedCreator.address);
        expect(bytes32ToString(material.title)).to.equal(MATERIAL_TITLE);
      });

      it("Should revert if category does not exist", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.createTrainingMaterial(
            MATERIAL_TITLE,
            999, // Non-existent category
            MATERIAL_CONTENT_IPFS,
            MATERIAL_PRICE_USDC
          )
        ).to.be.revertedWith("Category does not exist");
      });

      it("Should generate unique IDs for different materials", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        const tx1 = await contract.createTrainingMaterial(
          "First Material",
          1,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_PRICE_USDC
        );
        
        const tx2 = await contract.createTrainingMaterial(
          "Second Material",
          1,
          MATERIAL_CONTENT_IPFS,
          ethers.parseUnits("19.99", 6) // Different price
        );
        
        const receipt1 = await tx1.wait();
        const receipt2 = await tx2.wait();
        
        const event1 = receipt1.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const event2 = receipt2.logs.find(log => log.eventName === "TrainingMaterialCreated");
        
        const materialId1 = event1.args.materialId;
        const materialId2 = event2.args.materialId;
        
        expect(materialId1).to.not.equal(materialId2);
        expect(materialId1).to.be.a('bigint');
        expect(materialId2).to.be.a('bigint');
      });

      it("Should return the generated material ID", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        const tx = await contract.createTrainingMaterial(
          MATERIAL_TITLE,
          1,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_PRICE_USDC
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const generatedMaterialId = event.args.materialId;
        
        // Verify the material ID is a positive number
        expect(generatedMaterialId).to.be.a('bigint');
        expect(generatedMaterialId).to.be.greaterThan(0);
      });

      it("Should revert if title is empty", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.createTrainingMaterial(
            "", // Empty title
            1,
            MATERIAL_CONTENT_IPFS,
            MATERIAL_PRICE_USDC
          )
        ).to.be.revertedWith("Title cannot be empty");
      });



      it("Should revert if metadata URI is empty", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.createTrainingMaterial(
            MATERIAL_TITLE,
            1,
            "", // Empty metadata URI
            MATERIAL_PRICE_USDC
          )
        ).to.be.revertedWith("Metadata URI cannot be empty");
      });


      it("Should accept zero price for free materials", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        const tx = await contract.createTrainingMaterial(
          "Free Material",
          1,
          MATERIAL_CONTENT_IPFS,
          0 // Free material
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const generatedMaterialId = event.args.materialId;
        
        const material = await contract.getTrainingMaterial(generatedMaterialId);
        expect(material.priceUSDC).to.equal(0);
      });

      it("Should store correct price in USDC", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        const priceInUSDC = ethers.parseUnits("99.99", 6); // 99.99 USDC
        
        const tx = await contract.createTrainingMaterial(
          MATERIAL_TITLE,
          1,
          MATERIAL_CONTENT_IPFS,
          priceInUSDC
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const generatedMaterialId = event.args.materialId;
        
        const material = await contract.getTrainingMaterial(generatedMaterialId);
        expect(material.priceUSDC).to.equal(priceInUSDC);
        expect(ethers.formatUnits(material.priceUSDC, 6)).to.equal("99.99");
      });
    });

    describe("Deleting Training Materials", function () {
      async function deployWithMaterialFixture() {
        const fixture = await deployWithCategoryFixture();
        const { contract, owner, authorizedCreator } = fixture;
        
        // Authorize the creator and create a material
        await contract.authorizeCreator(authorizedCreator.address);
        
        const tx = await contract.connect(authorizedCreator).createTrainingMaterial(
          "Test Material",
          1,
          "test-content",
          ethers.parseUnits("10.99", 6)
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        fixture.testMaterialId = event.args.materialId;
        
        return fixture;
      }

      it("Should allow owner to delete any training material", async function () {
        const { contract, owner, authorizedCreator, testMaterialId } = await loadFixture(deployWithMaterialFixture);
        
        expect(await contract.getTotalMaterialCount()).to.equal(1);
        expect(await contract.trainingMaterialExists(testMaterialId)).to.be.true;
        
        await expect(contract.deleteTrainingMaterial(testMaterialId))
          .to.emit(contract, "TrainingMaterialDeleted")
          .withArgs(testMaterialId, owner.address, authorizedCreator.address);
        
        expect(await contract.getTotalMaterialCount()).to.equal(0);
        expect(await contract.trainingMaterialExists(testMaterialId)).to.be.false;
      });

      it("Should allow creator to delete their own training material", async function () {
        const { contract, authorizedCreator, testMaterialId } = await loadFixture(deployWithMaterialFixture);
        
        expect(await contract.getTotalMaterialCount()).to.equal(1);
        
        await expect(contract.connect(authorizedCreator).deleteTrainingMaterial(testMaterialId))
          .to.emit(contract, "TrainingMaterialDeleted")
          .withArgs(testMaterialId, authorizedCreator.address, authorizedCreator.address);
        
        expect(await contract.getTotalMaterialCount()).to.equal(0);
        expect(await contract.trainingMaterialExists(testMaterialId)).to.be.false;
      });

      it("Should not allow unauthorized users to delete training material", async function () {
        const { contract, otherAccount, testMaterialId } = await loadFixture(deployWithMaterialFixture);
        
        await expect(
          contract.connect(otherAccount).deleteTrainingMaterial(testMaterialId)
        ).to.be.revertedWith("Only owner or creator can delete this material");
      });

      it("Should revert when trying to delete non-existent material", async function () {
        const { contract } = await loadFixture(deployWithMaterialFixture);
        
        await expect(
          contract.deleteTrainingMaterial(999)
        ).to.be.revertedWith("Training material does not exist");
      });

      it("Should properly update category and total counts after deletion", async function () {
        const { contract, owner, testMaterialId } = await loadFixture(deployWithMaterialFixture);
        
        // Create another material in the same category
        const tx2 = await contract.createTrainingMaterial(
          "Second Material",
          1,
          "second-content",
          ethers.parseUnits("5.99", 6)
        );
        
        expect(await contract.getTotalMaterialCount()).to.equal(2);
        expect(await contract.getCategoryMaterialCount(1)).to.equal(2);
        
        // Delete first material
        await contract.deleteTrainingMaterial(testMaterialId);
        
        expect(await contract.getTotalMaterialCount()).to.equal(1);
        expect(await contract.getCategoryMaterialCount(1)).to.equal(1);
        
        // Verify the remaining material is still there
        const categoryMaterials = await contract.getTrainingMaterialsByCategory(1);
        expect(categoryMaterials.length).to.equal(1);
        expect(bytes32ToString(categoryMaterials[0].title)).to.equal("Second Material");
      });
    });

    describe("Training Material Queries", function () {
      async function deployWithMaterialsFixture() {
        const fixture = await deployWithCategoryFixture();
        const { contract } = fixture;
        
        // Create second category
        await contract.createCategory("Advanced Topics", "Advanced blockchain topics");
        
        // Create materials in different categories
        const tx1 = await contract.createTrainingMaterial(
          "Material 1",
          1,
          "ipfs-content-1",
          ethers.parseUnits("9.99", 6)
        );
        
        const tx2 = await contract.createTrainingMaterial(
          "Material 2",
          1,
          "ipfs-content-2",
          ethers.parseUnits("19.99", 6)
        );
        
        const tx3 = await contract.createTrainingMaterial(
          "Material 3",
          2,
          "ipfs-content-3",
          ethers.parseUnits("49.99", 6)
        );
        
        // Get the generated UUIDs from events
        const receipt1 = await tx1.wait();
        const receipt2 = await tx2.wait();
        const receipt3 = await tx3.wait();
        
        const event1 = receipt1.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const event2 = receipt2.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const event3 = receipt3.logs.find(log => log.eventName === "TrainingMaterialCreated");
        
        fixture.materialId1 = event1.args.materialId;
        fixture.materialId2 = event2.args.materialId;
        fixture.materialId3 = event3.args.materialId;
        
        return fixture;
      }

      it("Should return training materials by category", async function () {
        const { contract, materialId1, materialId2, materialId3 } = await loadFixture(deployWithMaterialsFixture);
        
        const category1Materials = await contract.getTrainingMaterialsByCategory(1);
        const category2Materials = await contract.getTrainingMaterialsByCategory(2);
        
        expect(category1Materials.length).to.equal(2);
        expect(category2Materials.length).to.equal(1);
        
        expect(category1Materials[0].id).to.equal(materialId1);
        expect(category1Materials[1].id).to.equal(materialId2);
        expect(category2Materials[0].id).to.equal(materialId3);
      });

      it("Should return category material count", async function () {
        const { contract } = await loadFixture(deployWithMaterialsFixture);
        
        expect(await contract.getCategoryMaterialCount(1)).to.equal(2);
        expect(await contract.getCategoryMaterialCount(2)).to.equal(1);
      });

      it("Should return all training materials", async function () {
        const { contract, materialId1, materialId2, materialId3 } = await loadFixture(deployWithMaterialsFixture);
        
        const allMaterials = await contract.getAllTrainingMaterials();
        expect(allMaterials.length).to.equal(3);
        
        expect(allMaterials[0].id).to.equal(materialId1);
        expect(allMaterials[1].id).to.equal(materialId2);
        expect(allMaterials[2].id).to.equal(materialId3);
      });

      it("Should check if training material exists", async function () {
        const { contract, materialId1 } = await loadFixture(deployWithMaterialsFixture);
        
        expect(await contract.trainingMaterialExists(materialId1)).to.be.true;
        expect(await contract.trainingMaterialExists(999)).to.be.false;
      });

      it("Should revert when querying non-existent training material", async function () {
        const { contract } = await loadFixture(deployWithMaterialsFixture);
        
        await expect(
          contract.getTrainingMaterial(999)
        ).to.be.revertedWith("Training material does not exist");
      });

      it("Should revert when querying materials from non-existent category", async function () {
        const { contract } = await loadFixture(deployWithMaterialsFixture);
        
        await expect(
          contract.getTrainingMaterialsByCategory(999)
        ).to.be.revertedWith("Category does not exist");
      });

      it("Should return training materials by creator", async function () {
        const { contract, owner, authorizedCreator } = await loadFixture(deployWithMaterialsFixture);
        
        // Authorize a new creator
        await contract.authorizeCreator(authorizedCreator.address);
        
        // Create a material with the new creator
        await contract.connect(authorizedCreator).createTrainingMaterial(
          "Creator Material",
          1,
          "ipfs-content-creator",
          ethers.parseUnits("25.99", 6)
        );
        
        // Check materials by owner (should have 3 from fixture)
        const ownerMaterials = await contract.getTrainingMaterialsByCreator(owner.address);
        expect(ownerMaterials.length).to.equal(3);
        
        // Check materials by authorized creator (should have 1)
        const creatorMaterials = await contract.getTrainingMaterialsByCreator(authorizedCreator.address);
        expect(creatorMaterials.length).to.equal(1);
        expect(bytes32ToString(creatorMaterials[0].title)).to.equal("Creator Material");
        expect(creatorMaterials[0].creator).to.equal(authorizedCreator.address);
      });

      it("Should return correct creator material count", async function () {
        const { contract, owner, authorizedCreator } = await loadFixture(deployWithMaterialsFixture);
        
        // Authorize a new creator and create materials
        await contract.authorizeCreator(authorizedCreator.address);
        
        await contract.connect(authorizedCreator).createTrainingMaterial(
          "Creator Material 1",
          1,
          "ipfs1",
          ethers.parseUnits("10.00", 6)
        );
        
        await contract.connect(authorizedCreator).createTrainingMaterial(
          "Creator Material 2",
          1,
          "ipfs2",
          ethers.parseUnits("20.00", 6)
        );
        
        expect(await contract.getCreatorMaterialCount(owner.address)).to.equal(3);
        expect(await contract.getCreatorMaterialCount(authorizedCreator.address)).to.equal(2);
      });
    });
  });

  describe("Integration Tests", function () {
    it("Should handle multiple categories and materials correctly", async function () {
      const { contract, owner } = await loadFixture(deployTrainingMaterialsFixture);
      
      // Create multiple categories
      await contract.createCategory("Beginner", "Beginner level content");
      await contract.createCategory("Intermediate", "Intermediate level content");
      await contract.createCategory("Advanced", "Advanced level content");
      
      // Create materials in each category
      await contract.createTrainingMaterial("Beginner 1", 1, "content1", ethers.parseUnits("5.99", 6));
      await contract.createTrainingMaterial("Beginner 2", 1, "content2", ethers.parseUnits("7.99", 6));
      await contract.createTrainingMaterial("Intermediate 1", 2, "content3", ethers.parseUnits("15.99", 6));
      await contract.createTrainingMaterial("Advanced 1", 3, "content4", ethers.parseUnits("29.99", 6));
      
      // Verify counts
      expect(await contract.getTotalMaterialCount()).to.equal(4);
      expect(await contract.getCategoryMaterialCount(1)).to.equal(2);
      expect(await contract.getCategoryMaterialCount(2)).to.equal(1);
      expect(await contract.getCategoryMaterialCount(3)).to.equal(1);
      
      // Verify all categories
      const categories = await contract.getAllCategories();
      expect(categories.length).to.equal(3);
      
      // Verify all materials
      const allMaterials = await contract.getAllTrainingMaterials();
      expect(allMaterials.length).to.equal(4);
      
      // Verify each material has all required fields
      for (const material of allMaterials) {
        expect(material.metadataURI).to.be.a('string');
        expect(material.metadataURI.length).to.be.greaterThan(0);
        expect(material.priceUSDC).to.be.a('bigint');
        expect(material.priceUSDC).to.be.greaterThan(0);
        expect(material.creator).to.be.a('string');
        expect(material.creator).to.equal(owner.address); // All created by owner in this test
      }
    });
  });
});