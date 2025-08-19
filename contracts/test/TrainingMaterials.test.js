import { expect } from "chai";
import hre from "hardhat";
import { loadFixture } from "@nomicfoundation/hardhat-toolbox/network-helpers.js";
const { ethers } = hre;

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
      expect(await contract.totalMaterials()).to.equal(0);
      
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
        expect(category.name).to.equal(CATEGORY_NAME);
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
        expect(category.name).to.equal(CATEGORY_NAME);
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
          MATERIAL_DESCRIPTION,
          1,
          MATERIAL_IMAGE_IPFS,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_CONTEXT_IPFS,
          MATERIAL_PRICE_USDC
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const generatedUuid = event.args.uuid;
        
        expect(generatedUuid).to.be.a('string');
        expect(generatedUuid.length).to.be.greaterThan(0);

        const material = await contract.getTrainingMaterial(generatedUuid);
        expect(material.uuid).to.equal(generatedUuid);
        expect(material.title).to.equal(MATERIAL_TITLE);
        expect(material.description).to.equal(MATERIAL_DESCRIPTION);
        expect(material.categoryId).to.equal(1);
        expect(material.imageIPFS).to.equal(MATERIAL_IMAGE_IPFS);
        expect(material.contentIPFS).to.equal(MATERIAL_CONTENT_IPFS);
        expect(material.contextFileIPFS).to.equal(MATERIAL_CONTEXT_IPFS);
        expect(material.priceUSDC).to.equal(MATERIAL_PRICE_USDC);
        expect(material.creator).to.equal(owner.address);
        expect(material.exists).to.be.true;
      });

      it("Should increment total materials count", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        expect(await contract.totalMaterials()).to.equal(0);
        
        await contract.createTrainingMaterial(
          MATERIAL_TITLE,
          MATERIAL_DESCRIPTION,
          1,
          MATERIAL_IMAGE_IPFS,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_CONTEXT_IPFS,
          MATERIAL_PRICE_USDC
        );

        expect(await contract.totalMaterials()).to.equal(1);
      });

      it("Should revert if non-authorized user tries to create training material", async function () {
        const { contract, otherAccount } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.connect(otherAccount).createTrainingMaterial(
            MATERIAL_TITLE,
            MATERIAL_DESCRIPTION,
            1,
            MATERIAL_IMAGE_IPFS,
            MATERIAL_CONTENT_IPFS,
            MATERIAL_CONTEXT_IPFS,
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
          MATERIAL_DESCRIPTION,
          1,
          MATERIAL_IMAGE_IPFS,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_CONTEXT_IPFS,
          MATERIAL_PRICE_USDC
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const generatedUuid = event.args.uuid;
        
        const material = await contract.getTrainingMaterial(generatedUuid);
        expect(material.creator).to.equal(authorizedCreator.address);
        expect(material.title).to.equal(MATERIAL_TITLE);
      });

      it("Should revert if category does not exist", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.createTrainingMaterial(
            MATERIAL_TITLE,
            MATERIAL_DESCRIPTION,
            999, // Non-existent category
            MATERIAL_IMAGE_IPFS,
            MATERIAL_CONTENT_IPFS,
            MATERIAL_CONTEXT_IPFS,
            MATERIAL_PRICE_USDC
          )
        ).to.be.revertedWith("Category does not exist");
      });

      it("Should generate unique UUIDs for different materials", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        const tx1 = await contract.createTrainingMaterial(
          "First Material",
          MATERIAL_DESCRIPTION,
          1,
          MATERIAL_IMAGE_IPFS,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_CONTEXT_IPFS,
          MATERIAL_PRICE_USDC
        );
        
        const tx2 = await contract.createTrainingMaterial(
          "Second Material",
          MATERIAL_DESCRIPTION,
          1,
          MATERIAL_IMAGE_IPFS,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_CONTEXT_IPFS,
          ethers.parseUnits("19.99", 6) // Different price
        );
        
        const receipt1 = await tx1.wait();
        const receipt2 = await tx2.wait();
        
        const event1 = receipt1.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const event2 = receipt2.logs.find(log => log.eventName === "TrainingMaterialCreated");
        
        const uuid1 = event1.args.uuid;
        const uuid2 = event2.args.uuid;
        
        expect(uuid1).to.not.equal(uuid2);
        expect(uuid1).to.be.a('string');
        expect(uuid2).to.be.a('string');
      });

      it("Should return the generated UUID", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        const tx = await contract.createTrainingMaterial(
          MATERIAL_TITLE,
          MATERIAL_DESCRIPTION,
          1,
          MATERIAL_IMAGE_IPFS,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_CONTEXT_IPFS,
          MATERIAL_PRICE_USDC
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const generatedUuid = event.args.uuid;
        
        // Verify the UUID follows a UUID-like format (has dashes)
        expect(generatedUuid).to.match(/^[a-f0-9]{16}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/);
      });

      it("Should revert if title is empty", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.createTrainingMaterial(
            "", // Empty title
            MATERIAL_DESCRIPTION,
            1,
            MATERIAL_IMAGE_IPFS,
            MATERIAL_CONTENT_IPFS,
            MATERIAL_CONTEXT_IPFS,
            MATERIAL_PRICE_USDC
          )
        ).to.be.revertedWith("Title cannot be empty");
      });

      it("Should revert if description is empty", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.createTrainingMaterial(
            MATERIAL_TITLE,
            "", // Empty description
            1,
            MATERIAL_IMAGE_IPFS,
            MATERIAL_CONTENT_IPFS,
            MATERIAL_CONTEXT_IPFS,
            MATERIAL_PRICE_USDC
          )
        ).to.be.revertedWith("Description cannot be empty");
      });

      it("Should revert if image IPFS is empty", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.createTrainingMaterial(
            MATERIAL_TITLE,
            MATERIAL_DESCRIPTION,
            1,
            "", // Empty image IPFS
            MATERIAL_CONTENT_IPFS,
            MATERIAL_CONTEXT_IPFS,
            MATERIAL_PRICE_USDC
          )
        ).to.be.revertedWith("Image IPFS hash cannot be empty");
      });

      it("Should revert if content IPFS is empty", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.createTrainingMaterial(
            MATERIAL_TITLE,
            MATERIAL_DESCRIPTION,
            1,
            MATERIAL_IMAGE_IPFS,
            "", // Empty content IPFS
            MATERIAL_CONTEXT_IPFS,
            MATERIAL_PRICE_USDC
          )
        ).to.be.revertedWith("Content IPFS hash cannot be empty");
      });

      it("Should revert if context file IPFS is empty", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        await expect(
          contract.createTrainingMaterial(
            MATERIAL_TITLE,
            MATERIAL_DESCRIPTION,
            1,
            MATERIAL_IMAGE_IPFS,
            MATERIAL_CONTENT_IPFS,
            "", // Empty context file IPFS
            MATERIAL_PRICE_USDC
          )
        ).to.be.revertedWith("Context file IPFS hash cannot be empty");
      });

      it("Should accept zero price for free materials", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        const tx = await contract.createTrainingMaterial(
          "Free Material",
          MATERIAL_DESCRIPTION,
          1,
          MATERIAL_IMAGE_IPFS,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_CONTEXT_IPFS,
          0 // Free material
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const generatedUuid = event.args.uuid;
        
        const material = await contract.getTrainingMaterial(generatedUuid);
        expect(material.priceUSDC).to.equal(0);
      });

      it("Should store correct price in USDC", async function () {
        const { contract } = await loadFixture(deployWithCategoryFixture);
        
        const priceInUSDC = ethers.parseUnits("99.99", 6); // 99.99 USDC
        
        const tx = await contract.createTrainingMaterial(
          MATERIAL_TITLE,
          MATERIAL_DESCRIPTION,
          1,
          MATERIAL_IMAGE_IPFS,
          MATERIAL_CONTENT_IPFS,
          MATERIAL_CONTEXT_IPFS,
          priceInUSDC
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const generatedUuid = event.args.uuid;
        
        const material = await contract.getTrainingMaterial(generatedUuid);
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
          "Test Description",
          1,
          "test-image",
          "test-content",
          "test-context",
          ethers.parseUnits("10.99", 6)
        );
        
        const receipt = await tx.wait();
        const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
        fixture.testUuid = event.args.uuid;
        
        return fixture;
      }

      it("Should allow owner to delete any training material", async function () {
        const { contract, owner, authorizedCreator, testUuid } = await loadFixture(deployWithMaterialFixture);
        
        expect(await contract.totalMaterials()).to.equal(1);
        expect(await contract.trainingMaterialExists(testUuid)).to.be.true;
        
        await expect(contract.deleteTrainingMaterial(testUuid))
          .to.emit(contract, "TrainingMaterialDeleted")
          .withArgs(testUuid, owner.address, authorizedCreator.address);
        
        expect(await contract.totalMaterials()).to.equal(0);
        expect(await contract.trainingMaterialExists(testUuid)).to.be.false;
      });

      it("Should allow creator to delete their own training material", async function () {
        const { contract, authorizedCreator, testUuid } = await loadFixture(deployWithMaterialFixture);
        
        expect(await contract.totalMaterials()).to.equal(1);
        
        await expect(contract.connect(authorizedCreator).deleteTrainingMaterial(testUuid))
          .to.emit(contract, "TrainingMaterialDeleted")
          .withArgs(testUuid, authorizedCreator.address, authorizedCreator.address);
        
        expect(await contract.totalMaterials()).to.equal(0);
        expect(await contract.trainingMaterialExists(testUuid)).to.be.false;
      });

      it("Should not allow unauthorized users to delete training material", async function () {
        const { contract, otherAccount, testUuid } = await loadFixture(deployWithMaterialFixture);
        
        await expect(
          contract.connect(otherAccount).deleteTrainingMaterial(testUuid)
        ).to.be.revertedWith("Only owner or creator can delete this material");
      });

      it("Should revert when trying to delete non-existent material", async function () {
        const { contract } = await loadFixture(deployWithMaterialFixture);
        
        await expect(
          contract.deleteTrainingMaterial("non-existent-uuid")
        ).to.be.revertedWith("Training material does not exist");
      });

      it("Should properly update category and total counts after deletion", async function () {
        const { contract, owner, testUuid } = await loadFixture(deployWithMaterialFixture);
        
        // Create another material in the same category
        const tx2 = await contract.createTrainingMaterial(
          "Second Material",
          "Second Description",
          1,
          "second-image",
          "second-content", 
          "second-context",
          ethers.parseUnits("5.99", 6)
        );
        
        expect(await contract.totalMaterials()).to.equal(2);
        expect(await contract.getCategoryMaterialCount(1)).to.equal(2);
        
        // Delete first material
        await contract.deleteTrainingMaterial(testUuid);
        
        expect(await contract.totalMaterials()).to.equal(1);
        expect(await contract.getCategoryMaterialCount(1)).to.equal(1);
        
        // Verify the remaining material is still there
        const categoryMaterials = await contract.getTrainingMaterialsByCategory(1);
        expect(categoryMaterials.length).to.equal(1);
        expect(categoryMaterials[0].title).to.equal("Second Material");
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
          "Description 1",
          1,
          "ipfs-image-1",
          "ipfs-content-1",
          "ipfs-context-1",
          ethers.parseUnits("9.99", 6)
        );
        
        const tx2 = await contract.createTrainingMaterial(
          "Material 2",
          "Description 2",
          1,
          "ipfs-image-2",
          "ipfs-content-2",
          "ipfs-context-2",
          ethers.parseUnits("19.99", 6)
        );
        
        const tx3 = await contract.createTrainingMaterial(
          "Material 3",
          "Description 3",
          2,
          "ipfs-image-3",
          "ipfs-content-3",
          "ipfs-context-3",
          ethers.parseUnits("49.99", 6)
        );
        
        // Get the generated UUIDs from events
        const receipt1 = await tx1.wait();
        const receipt2 = await tx2.wait();
        const receipt3 = await tx3.wait();
        
        const event1 = receipt1.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const event2 = receipt2.logs.find(log => log.eventName === "TrainingMaterialCreated");
        const event3 = receipt3.logs.find(log => log.eventName === "TrainingMaterialCreated");
        
        fixture.uuid1 = event1.args.uuid;
        fixture.uuid2 = event2.args.uuid;
        fixture.uuid3 = event3.args.uuid;
        
        return fixture;
      }

      it("Should return training materials by category", async function () {
        const { contract, uuid1, uuid2, uuid3 } = await loadFixture(deployWithMaterialsFixture);
        
        const category1Materials = await contract.getTrainingMaterialsByCategory(1);
        const category2Materials = await contract.getTrainingMaterialsByCategory(2);
        
        expect(category1Materials.length).to.equal(2);
        expect(category2Materials.length).to.equal(1);
        
        expect(category1Materials[0].uuid).to.equal(uuid1);
        expect(category1Materials[1].uuid).to.equal(uuid2);
        expect(category2Materials[0].uuid).to.equal(uuid3);
      });

      it("Should return category material count", async function () {
        const { contract } = await loadFixture(deployWithMaterialsFixture);
        
        expect(await contract.getCategoryMaterialCount(1)).to.equal(2);
        expect(await contract.getCategoryMaterialCount(2)).to.equal(1);
      });

      it("Should return all training materials", async function () {
        const { contract, uuid1, uuid2, uuid3 } = await loadFixture(deployWithMaterialsFixture);
        
        const allMaterials = await contract.getAllTrainingMaterials();
        expect(allMaterials.length).to.equal(3);
        
        expect(allMaterials[0].uuid).to.equal(uuid1);
        expect(allMaterials[1].uuid).to.equal(uuid2);
        expect(allMaterials[2].uuid).to.equal(uuid3);
      });

      it("Should check if training material exists", async function () {
        const { contract, uuid1 } = await loadFixture(deployWithMaterialsFixture);
        
        expect(await contract.trainingMaterialExists(uuid1)).to.be.true;
        expect(await contract.trainingMaterialExists("non-existent-uuid")).to.be.false;
      });

      it("Should revert when querying non-existent training material", async function () {
        const { contract } = await loadFixture(deployWithMaterialsFixture);
        
        await expect(
          contract.getTrainingMaterial("non-existent-uuid")
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
          "Material by authorized creator",
          1,
          "ipfs-image-creator",
          "ipfs-content-creator",
          "ipfs-context-creator",
          ethers.parseUnits("25.99", 6)
        );
        
        // Check materials by owner (should have 3 from fixture)
        const ownerMaterials = await contract.getTrainingMaterialsByCreator(owner.address);
        expect(ownerMaterials.length).to.equal(3);
        
        // Check materials by authorized creator (should have 1)
        const creatorMaterials = await contract.getTrainingMaterialsByCreator(authorizedCreator.address);
        expect(creatorMaterials.length).to.equal(1);
        expect(creatorMaterials[0].title).to.equal("Creator Material");
        expect(creatorMaterials[0].creator).to.equal(authorizedCreator.address);
      });

      it("Should return correct creator material count", async function () {
        const { contract, owner, authorizedCreator } = await loadFixture(deployWithMaterialsFixture);
        
        // Authorize a new creator and create materials
        await contract.authorizeCreator(authorizedCreator.address);
        
        await contract.connect(authorizedCreator).createTrainingMaterial(
          "Creator Material 1",
          "Description 1",
          1,
          "ipfs1", "ipfs1", "ipfs1",
          ethers.parseUnits("10.00", 6)
        );
        
        await contract.connect(authorizedCreator).createTrainingMaterial(
          "Creator Material 2",
          "Description 2",
          1,
          "ipfs2", "ipfs2", "ipfs2",
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
      await contract.createTrainingMaterial("Beginner 1", "Desc", 1, "img1", "content1", "context1", ethers.parseUnits("5.99", 6));
      await contract.createTrainingMaterial("Beginner 2", "Desc", 1, "img2", "content2", "context2", ethers.parseUnits("7.99", 6));
      await contract.createTrainingMaterial("Intermediate 1", "Desc", 2, "img3", "content3", "context3", ethers.parseUnits("15.99", 6));
      await contract.createTrainingMaterial("Advanced 1", "Desc", 3, "img4", "content4", "context4", ethers.parseUnits("29.99", 6));
      
      // Verify counts
      expect(await contract.totalMaterials()).to.equal(4);
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
        expect(material.contextFileIPFS).to.be.a('string');
        expect(material.contextFileIPFS.length).to.be.greaterThan(0);
        expect(material.priceUSDC).to.be.a('bigint');
        expect(material.priceUSDC).to.be.greaterThan(0);
        expect(material.creator).to.be.a('string');
        expect(material.creator).to.equal(owner.address); // All created by owner in this test
      }
    });
  });
});