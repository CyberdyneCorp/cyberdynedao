const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("CyberdyneAccessNFT", function () {
  let CyberdyneAccessNFT;
  let cyberdyneAccessNFT;
  let owner;
  let manager1;
  let manager2;
  let user1;
  let user2;
  let unauthorized;

  const NFT_NAME = "Cyberdyne Access Pass";
  const NFT_SYMBOL = "CYBACC";
  const BASE_URI = "https://api.cyberdyne.xyz/metadata/";

  beforeEach(async function () {
    // Get signers
    [owner, manager1, manager2, user1, user2, unauthorized] = await ethers.getSigners();

    // Deploy the contract
    CyberdyneAccessNFT = await ethers.getContractFactory("CyberdyneAccessNFT");
    cyberdyneAccessNFT = await CyberdyneAccessNFT.deploy(NFT_NAME, NFT_SYMBOL, BASE_URI);
    await cyberdyneAccessNFT.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await cyberdyneAccessNFT.owner()).to.equal(owner.address);
    });

    it("Should set correct NFT metadata", async function () {
      expect(await cyberdyneAccessNFT.name()).to.equal(NFT_NAME);
      expect(await cyberdyneAccessNFT.symbol()).to.equal(NFT_SYMBOL);
    });

    it("Should initialize with zero total supply", async function () {
      expect(await cyberdyneAccessNFT.totalSupply()).to.equal(0);
      expect(await cyberdyneAccessNFT.getNextTokenId()).to.equal(1);
    });

    it("Should authorize owner as manager", async function () {
      expect(await cyberdyneAccessNFT.isAuthorizedManager(owner.address)).to.be.true;
    });
  });

  describe("Manager Authorization", function () {
    it("Should allow owner to authorize managers", async function () {
      await cyberdyneAccessNFT.authorizeManager(manager1.address);
      expect(await cyberdyneAccessNFT.isAuthorizedManager(manager1.address)).to.be.true;
    });

    it("Should emit ManagerAuthorized event", async function () {
      await expect(cyberdyneAccessNFT.authorizeManager(manager1.address))
        .to.emit(cyberdyneAccessNFT, "ManagerAuthorized")
        .withArgs(manager1.address, owner.address);
    });

    it("Should not allow non-owner to authorize managers", async function () {
      await expect(
        cyberdyneAccessNFT.connect(manager1).authorizeManager(manager2.address)
      ).to.be.revertedWithCustomError(cyberdyneAccessNFT, "OwnableUnauthorizedAccount");
    });

    it("Should not allow authorizing the same manager twice", async function () {
      await cyberdyneAccessNFT.authorizeManager(manager1.address);
      await expect(
        cyberdyneAccessNFT.authorizeManager(manager1.address)
      ).to.be.revertedWith("Manager already authorized");
    });

    it("Should allow owner to deauthorize managers", async function () {
      await cyberdyneAccessNFT.authorizeManager(manager1.address);
      await cyberdyneAccessNFT.deauthorizeManager(manager1.address);
      expect(await cyberdyneAccessNFT.isAuthorizedManager(manager1.address)).to.be.false;
    });

    it("Should not allow deauthorizing the owner", async function () {
      await expect(
        cyberdyneAccessNFT.deauthorizeManager(owner.address)
      ).to.be.revertedWith("Cannot deauthorize contract owner");
    });

    it("Should return authorized managers list", async function () {
      await cyberdyneAccessNFT.authorizeManager(manager1.address);
      await cyberdyneAccessNFT.authorizeManager(manager2.address);
      
      const managers = await cyberdyneAccessNFT.getAuthorizedManagers();
      expect(managers).to.include(owner.address);
      expect(managers).to.include(manager1.address);
      expect(managers).to.include(manager2.address);
    });
  });

  describe("NFT Minting", function () {
    it("Should allow owner to mint NFTs", async function () {
      const tx = await cyberdyneAccessNFT.mint(
        user1.address,
        true,  // learning access
        false, // frontend access
        true,  // backend access
        "custom-metadata-uri"
      );

      const receipt = await tx.wait();
      const event = receipt.logs.find(log => log.eventName === "NFTMinted");
      
      expect(event.args.tokenId).to.equal(1);
      expect(event.args.to).to.equal(user1.address);
      expect(event.args.learningMaterials).to.be.true;
      expect(event.args.frontendServers).to.be.false;
      expect(event.args.backendServers).to.be.true;
    });

    it("Should not allow non-owner to mint NFTs", async function () {
      await expect(
        cyberdyneAccessNFT.connect(manager1).mint(
          user1.address,
          true, false, true,
          "metadata-uri"
        )
      ).to.be.revertedWithCustomError(cyberdyneAccessNFT, "OwnableUnauthorizedAccount");
    });

    it("Should increment token ID and total supply", async function () {
      await cyberdyneAccessNFT.mint(user1.address, true, false, true, "uri1");
      await cyberdyneAccessNFT.mint(user2.address, false, true, false, "uri2");

      expect(await cyberdyneAccessNFT.totalSupply()).to.equal(2);
      expect(await cyberdyneAccessNFT.getNextTokenId()).to.equal(3);
    });

    it("Should set correct permissions for minted NFT", async function () {
      await cyberdyneAccessNFT.mint(user1.address, true, false, true, "test-uri");
      
      const permissions = await cyberdyneAccessNFT.getTokenPermissions(1);
      expect(permissions.learningMaterials).to.be.true;
      expect(permissions.frontendServers).to.be.false;
      expect(permissions.backendServers).to.be.true;
      expect(permissions.metadataURI).to.equal("test-uri");
    });

    it("Should support batch minting", async function () {
      const recipients = [user1.address, user2.address];
      const learning = [true, false];
      const frontend = [false, true];
      const backend = [true, false];
      const uris = ["uri1", "uri2"];

      const tokenIds = await cyberdyneAccessNFT.batchMint(
        recipients, learning, frontend, backend, uris
      );

      expect(tokenIds.length).to.equal(2);
      expect(await cyberdyneAccessNFT.totalSupply()).to.equal(2);
      expect(await cyberdyneAccessNFT.ownerOf(tokenIds[0])).to.equal(user1.address);
      expect(await cyberdyneAccessNFT.ownerOf(tokenIds[1])).to.equal(user2.address);
    });
  });

  describe("Permission Management", function () {
    let tokenId;

    beforeEach(async function () {
      const tx = await cyberdyneAccessNFT.mint(
        user1.address,
        true, false, true,
        "initial-uri"
      );
      const receipt = await tx.wait();
      const event = receipt.logs.find(log => log.eventName === "NFTMinted");
      tokenId = event.args.tokenId;

      // Authorize manager1 for permission updates
      await cyberdyneAccessNFT.authorizeManager(manager1.address);
    });

    it("Should allow authorized managers to update permissions", async function () {
      await cyberdyneAccessNFT.connect(manager1).updatePermissions(
        tokenId,
        false, // learning
        true,  // frontend
        false  // backend
      );

      const permissions = await cyberdyneAccessNFT.getTokenPermissions(tokenId);
      expect(permissions.learningMaterials).to.be.false;
      expect(permissions.frontendServers).to.be.true;
      expect(permissions.backendServers).to.be.false;
    });

    it("Should allow owner to update permissions", async function () {
      await cyberdyneAccessNFT.connect(owner).updatePermissions(
        tokenId,
        false, true, false
      );

      const permissions = await cyberdyneAccessNFT.getTokenPermissions(tokenId);
      expect(permissions.learningMaterials).to.be.false;
      expect(permissions.frontendServers).to.be.true;
      expect(permissions.backendServers).to.be.false;
    });

    it("Should not allow unauthorized users to update permissions", async function () {
      await expect(
        cyberdyneAccessNFT.connect(unauthorized).updatePermissions(
          tokenId,
          false, true, false
        )
      ).to.be.revertedWith("Not authorized to manage permissions");
    });

    it("Should emit PermissionsUpdated event", async function () {
      await expect(
        cyberdyneAccessNFT.connect(manager1).updatePermissions(
          tokenId,
          false, true, false
        )
      ).to.emit(cyberdyneAccessNFT, "PermissionsUpdated")
       .withArgs(tokenId, false, true, false, manager1.address);
    });

    it("Should allow updating metadata", async function () {
      const newURI = "updated-metadata-uri";
      await cyberdyneAccessNFT.connect(manager1).updateMetadata(tokenId, newURI);

      const permissions = await cyberdyneAccessNFT.getTokenPermissions(tokenId);
      expect(permissions.metadataURI).to.equal(newURI);
    });

    it("Should support batch permission updates", async function () {
      // Mint another NFT
      await cyberdyneAccessNFT.mint(user2.address, false, false, false, "uri2");
      
      const tokenIds = [1, 2];
      const learning = [true, false];
      const frontend = [false, true];
      const backend = [true, false];

      await cyberdyneAccessNFT.connect(manager1).batchUpdatePermissions(
        tokenIds, learning, frontend, backend
      );

      const perms1 = await cyberdyneAccessNFT.getTokenPermissions(1);
      const perms2 = await cyberdyneAccessNFT.getTokenPermissions(2);
      
      expect(perms1.learningMaterials).to.be.true;
      expect(perms1.frontendServers).to.be.false;
      expect(perms1.backendServers).to.be.true;
      
      expect(perms2.learningMaterials).to.be.false;
      expect(perms2.frontendServers).to.be.true;
      expect(perms2.backendServers).to.be.false;
    });
  });

  describe("Access Checking", function () {
    beforeEach(async function () {
      // Mint NFTs with different permissions
      await cyberdyneAccessNFT.mint(user1.address, true, false, true, "uri1");   // Token 1
      await cyberdyneAccessNFT.mint(user1.address, false, true, false, "uri2");  // Token 2
      await cyberdyneAccessNFT.mint(user2.address, false, false, true, "uri3");  // Token 3
    });

    it("Should check individual token permissions correctly", async function () {
      expect(await cyberdyneAccessNFT.hasLearningAccess(1)).to.be.true;
      expect(await cyberdyneAccessNFT.hasFrontendAccess(1)).to.be.false;
      expect(await cyberdyneAccessNFT.hasBackendAccess(1)).to.be.true;

      expect(await cyberdyneAccessNFT.hasLearningAccess(2)).to.be.false;
      expect(await cyberdyneAccessNFT.hasFrontendAccess(2)).to.be.true;
      expect(await cyberdyneAccessNFT.hasBackendAccess(2)).to.be.false;
    });

    it("Should check access by string type", async function () {
      expect(await cyberdyneAccessNFT.hasAccess(1, "learning")).to.be.true;
      expect(await cyberdyneAccessNFT.hasAccess(1, "frontend")).to.be.false;
      expect(await cyberdyneAccessNFT.hasAccess(1, "backend")).to.be.true;
      expect(await cyberdyneAccessNFT.hasAccess(1, "invalid")).to.be.false;
    });

    it("Should check address-based access correctly", async function () {
      // user1 has tokens 1 and 2 with different permissions
      expect(await cyberdyneAccessNFT.addressHasLearningAccess(user1.address)).to.be.true;  // Token 1
      expect(await cyberdyneAccessNFT.addressHasFrontendAccess(user1.address)).to.be.true;  // Token 2
      expect(await cyberdyneAccessNFT.addressHasBackendAccess(user1.address)).to.be.true;   // Token 1

      // user2 has token 3 with only backend access
      expect(await cyberdyneAccessNFT.addressHasLearningAccess(user2.address)).to.be.false;
      expect(await cyberdyneAccessNFT.addressHasFrontendAccess(user2.address)).to.be.false;
      expect(await cyberdyneAccessNFT.addressHasBackendAccess(user2.address)).to.be.true;   // Token 3

      // unauthorized has no tokens
      expect(await cyberdyneAccessNFT.addressHasLearningAccess(unauthorized.address)).to.be.false;
      expect(await cyberdyneAccessNFT.addressHasFrontendAccess(unauthorized.address)).to.be.false;
      expect(await cyberdyneAccessNFT.addressHasBackendAccess(unauthorized.address)).to.be.false;
    });

    it("Should revert for non-existent tokens", async function () {
      await expect(
        cyberdyneAccessNFT.hasLearningAccess(999)
      ).to.be.revertedWith("Token does not exist");
    });
  });

  describe("User Token Queries", function () {
    beforeEach(async function () {
      await cyberdyneAccessNFT.mint(user1.address, true, false, true, "uri1");   // Token 1
      await cyberdyneAccessNFT.mint(user1.address, false, true, false, "uri2");  // Token 2
      await cyberdyneAccessNFT.mint(user2.address, true, true, true, "uri3");    // Token 3
    });

    it("Should return user tokens correctly", async function () {
      const user1Tokens = await cyberdyneAccessNFT.getUserTokens(user1.address);
      const user2Tokens = await cyberdyneAccessNFT.getUserTokens(user2.address);

      expect(user1Tokens.length).to.equal(2);
      expect(user1Tokens).to.deep.equal([1n, 2n]);
      
      expect(user2Tokens.length).to.equal(1);
      expect(user2Tokens).to.deep.equal([3n]);
    });

    it("Should return user permissions correctly", async function () {
      const [tokenIds, permissions] = await cyberdyneAccessNFT.getUserPermissions(user1.address);

      expect(tokenIds.length).to.equal(2);
      expect(tokenIds).to.deep.equal([1n, 2n]);
      
      expect(permissions.length).to.equal(2);
      expect(permissions[0].learningMaterials).to.be.true;
      expect(permissions[0].frontendServers).to.be.false;
      expect(permissions[0].backendServers).to.be.true;
      
      expect(permissions[1].learningMaterials).to.be.false;
      expect(permissions[1].frontendServers).to.be.true;
      expect(permissions[1].backendServers).to.be.false;
    });

    it("Should return empty arrays for users with no tokens", async function () {
      const tokens = await cyberdyneAccessNFT.getUserTokens(unauthorized.address);
      const [tokenIds, permissions] = await cyberdyneAccessNFT.getUserPermissions(unauthorized.address);

      expect(tokens.length).to.equal(0);
      expect(tokenIds.length).to.equal(0);
      expect(permissions.length).to.equal(0);
    });
  });

  describe("Token URI and Metadata", function () {
    let tokenId;

    beforeEach(async function () {
      const tx = await cyberdyneAccessNFT.mint(
        user1.address,
        true, false, true,
        "custom-metadata-uri"
      );
      const receipt = await tx.wait();
      const event = receipt.logs.find(log => log.eventName === "NFTMinted");
      tokenId = event.args.tokenId;
    });

    it("Should return custom metadata URI when set", async function () {
      const tokenURI = await cyberdyneAccessNFT.tokenURI(tokenId);
      expect(tokenURI).to.equal("custom-metadata-uri");
    });

    it("Should return base URI when no custom URI is set", async function () {
      await cyberdyneAccessNFT.mint(user2.address, false, true, false, "");
      const tokenURI = await cyberdyneAccessNFT.tokenURI(2);
      expect(tokenURI).to.equal(BASE_URI + "2");
    });

    it("Should allow owner to update base URI", async function () {
      const newBaseURI = "https://new-api.cyberdyne.xyz/metadata/";
      await cyberdyneAccessNFT.setBaseURI(newBaseURI);
      
      await cyberdyneAccessNFT.mint(user2.address, false, true, false, "");
      const tokenURI = await cyberdyneAccessNFT.tokenURI(2);
      expect(tokenURI).to.equal(newBaseURI + "2");
    });

    it("Should update metadata URI correctly", async function () {
      await cyberdyneAccessNFT.authorizeManager(manager1.address);
      const newURI = "updated-custom-uri";
      
      await cyberdyneAccessNFT.connect(manager1).updateMetadata(tokenId, newURI);
      
      const tokenURI = await cyberdyneAccessNFT.tokenURI(tokenId);
      expect(tokenURI).to.equal(newURI);
    });
  });

  describe("Contract Ownership", function () {
    it("Should transfer ownership correctly", async function () {
      await cyberdyneAccessNFT.transferContractOwnership(manager1.address);
      
      expect(await cyberdyneAccessNFT.owner()).to.equal(manager1.address);
      expect(await cyberdyneAccessNFT.isAuthorizedManager(manager1.address)).to.be.true;
    });

    it("Should not allow transferring to same owner", async function () {
      await expect(
        cyberdyneAccessNFT.transferContractOwnership(owner.address)
      ).to.be.revertedWith("New owner cannot be the same as current owner");
    });

    it("Should not allow transferring to zero address", async function () {
      await expect(
        cyberdyneAccessNFT.transferContractOwnership(ethers.ZeroAddress)
      ).to.be.revertedWith("New owner cannot be zero address");
    });
  });

  describe("Edge Cases and Utility Functions", function () {
    it("Should check token existence correctly", async function () {
      expect(await cyberdyneAccessNFT.exists(1)).to.be.false;
      
      await cyberdyneAccessNFT.mint(user1.address, true, false, true, "uri");
      
      expect(await cyberdyneAccessNFT.exists(1)).to.be.true;
      expect(await cyberdyneAccessNFT.exists(2)).to.be.false;
    });

    it("Should handle ERC721Enumerable functions correctly", async function () {
      await cyberdyneAccessNFT.mint(user1.address, true, false, true, "uri1");
      await cyberdyneAccessNFT.mint(user1.address, false, true, false, "uri2");
      
      expect(await cyberdyneAccessNFT.balanceOf(user1.address)).to.equal(2);
      expect(await cyberdyneAccessNFT.tokenOfOwnerByIndex(user1.address, 0)).to.equal(1);
      expect(await cyberdyneAccessNFT.tokenOfOwnerByIndex(user1.address, 1)).to.equal(2);
      expect(await cyberdyneAccessNFT.tokenByIndex(0)).to.equal(1);
      expect(await cyberdyneAccessNFT.tokenByIndex(1)).to.equal(2);
    });

    it("Should support interface detection correctly", async function () {
      // ERC721 interface
      expect(await cyberdyneAccessNFT.supportsInterface("0x80ac58cd")).to.be.true;
      // ERC721Enumerable interface  
      expect(await cyberdyneAccessNFT.supportsInterface("0x780e9d63")).to.be.true;
      // Invalid interface
      expect(await cyberdyneAccessNFT.supportsInterface("0x12345678")).to.be.false;
    });

    it("Should handle permission updates after token transfers", async function () {
      await cyberdyneAccessNFT.mint(user1.address, true, false, true, "uri");
      await cyberdyneAccessNFT.authorizeManager(manager1.address);
      
      // Transfer token from user1 to user2
      await cyberdyneAccessNFT.connect(user1).transferFrom(user1.address, user2.address, 1);
      
      // Check that user2 now has the permissions
      expect(await cyberdyneAccessNFT.addressHasLearningAccess(user1.address)).to.be.false;
      expect(await cyberdyneAccessNFT.addressHasLearningAccess(user2.address)).to.be.true;
      
      // Manager should still be able to update permissions
      await cyberdyneAccessNFT.connect(manager1).updatePermissions(1, false, true, false);
      
      const permissions = await cyberdyneAccessNFT.getTokenPermissions(1);
      expect(permissions.learningMaterials).to.be.false;
      expect(permissions.frontendServers).to.be.true;
    });
  });
});