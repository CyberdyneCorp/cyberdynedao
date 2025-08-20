import { expect } from "chai";
import hre from "hardhat";
const { ethers } = hre;

describe("UUID Generation Tests", function () {
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

  describe("UUID Format Validation", function () {
    it("Should generate valid UUID format", async function () {
      const tx = await products.connect(creator).createProduct(
        "Test Product",
        1,
        ethers.parseUnits("100", 6),
        "QmTestIPFS"
      );
      const receipt = await tx.wait();
      const uuid = receipt.logs[0].args.uuid;

      console.log("Generated UUID:", uuid);
      
      // UUID should match format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
      expect(uuid).to.match(uuidRegex, "UUID should match standard format");
      
      // Check length
      expect(uuid).to.have.length(36, "UUID should be 36 characters long");
      
      // Check hyphen positions
      expect(uuid[8]).to.equal('-');
      expect(uuid[13]).to.equal('-');
      expect(uuid[18]).to.equal('-');
      expect(uuid[23]).to.equal('-');
    });

    it("Should generate different UUIDs for different products", async function () {
      const tx1 = await products.connect(creator).createProduct(
        "Product 1",
        1,
        ethers.parseUnits("100", 6),
        "QmTestIPFS1"
      );
      const receipt1 = await tx1.wait();
      const uuid1 = receipt1.logs[0].args.uuid;

      const tx2 = await products.connect(creator).createProduct(
        "Product 2", 
        1,
        ethers.parseUnits("200", 6),
        "QmTestIPFS2"
      );
      const receipt2 = await tx2.wait();
      const uuid2 = receipt2.logs[0].args.uuid;

      expect(uuid1).to.not.equal(uuid2, "Different products should have different UUIDs");
    });

    it("Should generate valid hex characters only", async function () {
      const tx = await products.connect(creator).createProduct(
        "Hex Test Product",
        1,
        ethers.parseUnits("100", 6),
        "QmTestIPFS"
      );
      const receipt = await tx.wait();
      const uuid = receipt.logs[0].args.uuid;

      console.log("UUID for hex validation:", uuid);

      // Remove hyphens and check if all characters are valid hex
      const hexPart = uuid.replace(/-/g, '');
      const validHexRegex = /^[0-9a-f]+$/;
      expect(hexPart).to.match(validHexRegex, "UUID should contain only valid hex characters (0-9, a-f)");
    });

    it("Should not contain invalid characters", async function () {
      const tx = await products.connect(creator).createProduct(
        "Character Test",
        1,
        ethers.parseUnits("100", 6),
        "QmTestIPFS"
      );
      const receipt = await tx.wait();
      const uuid = receipt.logs[0].args.uuid;

      // Check for any characters outside valid hex range
      const hexPart = uuid.replace(/-/g, '');
      for (let i = 0; i < hexPart.length; i++) {
        const char = hexPart[i];
        const isValid = (char >= '0' && char <= '9') || (char >= 'a' && char <= 'f');
        expect(isValid, `Character '${char}' at position ${i} is not valid hex`).to.be.true;
      }
    });

    it("Should handle edge cases with boundary values", async function () {
      // Test with maximum values and different inputs to stress test hex conversion
      const testCases = [
        "A".repeat(100), // Long string
        "Test with numbers 123456789",
        "Special chars !@#$%^&*()",
        "", // This should fail validation, but test hex generation
        "Single char: Z"
      ];

      for (let i = 0; i < testCases.length; i++) {
        const title = testCases[i] || `Test Product ${i}`;
        
        try {
          const tx = await products.connect(creator).createProduct(
            title,
            1,
            ethers.parseUnits("100", 6),
            "QmTestIPFS"
          );
          const receipt = await tx.wait();
          const uuid = receipt.logs[0].args.uuid;
          
          console.log(`UUID for "${title.substring(0, 20)}...":`, uuid);
          
          // Validate format
          const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
          expect(uuid).to.match(uuidRegex, `UUID should be valid for input: ${title.substring(0, 20)}`);
          
        } catch (error) {
          // If the transaction fails due to empty title, that's expected
          if (!title.trim()) {
            expect(error.message).to.include("Title cannot be empty");
          } else {
            throw error;
          }
        }
      }
    });

    it("Should maintain consistency in hex character case", async function () {
      const tx = await products.connect(creator).createProduct(
        "Case Test Product",
        1,
        ethers.parseUnits("100", 6),
        "QmTestIPFS"
      );
      const receipt = await tx.wait();
      const uuid = receipt.logs[0].args.uuid;

      const hexPart = uuid.replace(/-/g, '');
      
      // All hex letters should be lowercase
      for (let i = 0; i < hexPart.length; i++) {
        const char = hexPart[i];
        if (char >= 'A' && char <= 'F') {
          expect.fail(`Found uppercase hex character '${char}' at position ${i}. All hex should be lowercase.`);
        }
        if ((char >= 'a' && char <= 'f') || (char >= '0' && char <= '9')) {
          // Valid hex character
          continue;
        } else {
          expect.fail(`Found invalid character '${char}' at position ${i}`);
        }
      }
    });
  });

  describe("UUID Collision Testing", function () {
    it("Should generate unique UUIDs for rapid sequential creation", async function () {
      const uuids = new Set();
      const numTests = 10;

      for (let i = 0; i < numTests; i++) {
        const tx = await products.connect(creator).createProduct(
          `Rapid Test ${i}`,
          1,
          ethers.parseUnits("100", 6),
          `QmTestIPFS${i}`
        );
        const receipt = await tx.wait();
        const uuid = receipt.logs[0].args.uuid;

        expect(uuids.has(uuid), `UUID collision detected: ${uuid}`).to.be.false;
        uuids.add(uuid);
      }

      expect(uuids.size).to.equal(numTests, "Should have generated unique UUIDs for all products");
    });
  });
});