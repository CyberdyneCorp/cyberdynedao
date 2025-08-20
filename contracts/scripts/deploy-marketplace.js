import hre from "hardhat";
const { ethers } = hre;

async function main() {
  const [deployer, feeRecipient] = await ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", ethers.formatEther(await ethers.provider.getBalance(deployer.address)));

  // Configuration
  const MARKETPLACE_FEE_PERCENT = 250; // 2.5%
  const USDC_DECIMALS = 6;
  
  // For testnet/local: Deploy mock USDC, for mainnet: use real USDC address
  let usdcAddress;
  
  if (hre.network.name === "hardhat" || hre.network.name === "localhost") {
    console.log("\n🪙 Deploying Mock USDC for testing...");
    const MockERC20 = await ethers.getContractFactory("MockERC20");
    const mockUSDC = await MockERC20.deploy(ethers.parseUnits("1000000", USDC_DECIMALS)); // 1M USDC
    await mockUSDC.waitForDeployment();
    usdcAddress = await mockUSDC.getAddress();
    console.log("Mock USDC deployed to:", usdcAddress);
  } else {
    // Real USDC addresses for different networks
    const USDC_ADDRESSES = {
      mainnet: "0xA0b86a33E6441b4b90673f096cD8a5E4fE8CDAC8", // Real USDC on mainnet
      base: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",    // USDC on Base
      arbitrum: "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", // USDC on Arbitrum
      polygon: "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",  // USDC on Polygon
    };
    
    usdcAddress = USDC_ADDRESSES[hre.network.name];
    if (!usdcAddress) {
      throw new Error(`No USDC address configured for network: ${hre.network.name}`);
    }
    console.log(`Using USDC at: ${usdcAddress} for ${hre.network.name}`);
  }

  // Check if other contracts are already deployed
  let productsAddress, accessNFTAddress;

  // Try to load existing deployments
  try {
    const productsDeployment = require(`../deployments/CyberdyneProducts-${hre.network.name}.json`);
    productsAddress = productsDeployment.address;
    console.log("Using existing CyberdyneProducts at:", productsAddress);
  } catch (error) {
    console.log("\n📦 Deploying CyberdyneProducts...");
    const CyberdyneProducts = await ethers.getContractFactory("CyberdyneProducts");
    const products = await CyberdyneProducts.deploy();
    await products.waitForDeployment();
    productsAddress = await products.getAddress();
    console.log("CyberdyneProducts deployed to:", productsAddress);
  }


  try {
    const accessDeployment = require(`../deployments/CyberdyneAccessNFT-${hre.network.name}.json`);
    accessNFTAddress = accessDeployment.address;
    console.log("Using existing CyberdyneAccessNFT at:", accessNFTAddress);
  } catch (error) {
    console.log("\n🎫 Deploying CyberdyneAccessNFT...");
    const CyberdyneAccessNFT = await ethers.getContractFactory("CyberdyneAccessNFT");
    const accessNFT = await CyberdyneAccessNFT.deploy(
      "Cyberdyne Access Pass",
      "CYBACC",
      "https://api.cyberdyne.xyz/metadata/"
    );
    await accessNFT.waitForDeployment();
    accessNFTAddress = await accessNFT.getAddress();
    console.log("CyberdyneAccessNFT deployed to:", accessNFTAddress);
  }

  // Deploy CyberdyneMarketplace
  console.log("\n🏪 Deploying CyberdyneMarketplace...");
  const CyberdyneMarketplace = await ethers.getContractFactory("CyberdyneMarketplace");
  const marketplace = await CyberdyneMarketplace.deploy(
    usdcAddress,
    productsAddress,
    accessNFTAddress,
    MARKETPLACE_FEE_PERCENT,
    feeRecipient ? feeRecipient.address : deployer.address // Use deployer as fee recipient if not provided
  );

  await marketplace.waitForDeployment();
  const marketplaceAddress = await marketplace.getAddress();

  console.log("\n✅ Deployment Summary:");
  console.log("=====================");
  console.log("Network:", hre.network.name);
  console.log("Deployer:", deployer.address);
  console.log("USDC Token:", usdcAddress);
  console.log("CyberdyneProducts:", productsAddress);
  console.log("CyberdyneAccessNFT:", accessNFTAddress);
  console.log("CyberdyneMarketplace:", marketplaceAddress);
  console.log("Marketplace Fee:", `${MARKETPLACE_FEE_PERCENT / 100}%`);
  console.log("Fee Recipient:", feeRecipient ? feeRecipient.address : deployer.address);

  // Save deployment info
  const deploymentInfo = {
    address: marketplaceAddress,
    deployer: deployer.address,
    deploymentBlock: await ethers.provider.getBlockNumber(),
    deploymentTime: new Date().toISOString(),
    network: hre.network.name,
    dependencies: {
      usdcToken: usdcAddress,
      cyberdyneProducts: productsAddress,
      cyberdyneAccessNFT: accessNFTAddress
    },
    configuration: {
      marketplaceFeePercent: MARKETPLACE_FEE_PERCENT,
      feeRecipient: feeRecipient ? feeRecipient.address : deployer.address
    }
  };

  // Write deployment file
  const fs = await import('fs');
  const path = await import('path');
  const deploymentsDir = path.resolve('./deployments');
  
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir, { recursive: true });
  }

  const deploymentPath = path.resolve(deploymentsDir, `CyberdyneMarketplace-${hre.network.name}.json`);
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));

  console.log("\n📄 Deployment info saved to:", deploymentPath);

  // Verify contracts on Etherscan if not on local network
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("\n🔍 Waiting for block confirmations...");
    await marketplace.deploymentTransaction().wait(5);

    console.log("Verifying contract on Etherscan...");
    try {
      await hre.run("verify:verify", {
        address: marketplaceAddress,
        constructorArguments: [
          usdcAddress,
          productsAddress,
          accessNFTAddress,
          MARKETPLACE_FEE_PERCENT,
          feeRecipient ? feeRecipient.address : deployer.address
        ],
      });
      console.log("✅ Contract verified on Etherscan");
    } catch (error) {
      console.log("❌ Verification failed:", error.message);
    }
  }

  // If on local network, provide some helpful setup commands
  if (hre.network.name === "hardhat" || hre.network.name === "localhost") {
    console.log("\n🛠️  Local Setup Commands:");
    console.log("========================");
    console.log("// Get contract instances");
    console.log(`const marketplace = await ethers.getContractAt("CyberdyneMarketplace", "${marketplaceAddress}");`);
    console.log(`const usdcToken = await ethers.getContractAt("MockERC20", "${usdcAddress}");`);
    console.log(`const products = await ethers.getContractAt("CyberdyneProducts", "${productsAddress}");`);
    console.log(`const accessNFT = await ethers.getContractAt("CyberdyneAccessNFT", "${accessNFTAddress}");`);
    console.log("\n// Example: Create a seller with marketplace permissions");
    console.log("const [owner, seller] = await ethers.getSigners();");
    console.log("await accessNFT.mint(seller.address, false, false, false, false, false, true, '');");
    console.log("await products.authorizeCreator(seller.address);");
  }
}

// Error handling
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Deployment failed:", error);
    process.exit(1);
  });