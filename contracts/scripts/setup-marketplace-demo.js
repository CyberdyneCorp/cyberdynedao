import hre from "hardhat";
const { ethers } = hre;

async function main() {
  console.log("🚀 Setting up CyberdyneMarketplace Demo Environment");
  console.log("==================================================");

  // Get signers
  const [deployer, seller1, seller2, buyer1, buyer2] = await ethers.getSigners();

  // Load deployed contract addresses
  const deploymentPath = `./deployments/CyberdyneMarketplace-${hre.network.name}.json`;
  let deployment;
  
  try {
    deployment = require(deploymentPath);
  } catch (error) {
    console.error("❌ Marketplace deployment not found. Please run deploy-marketplace.js first");
    process.exit(1);
  }

  // Get contract instances
  const marketplace = await ethers.getContractAt("CyberdyneMarketplace", deployment.address);
  const usdcToken = await ethers.getContractAt("MockERC20", deployment.dependencies.usdcToken);
  const products = await ethers.getContractAt("CyberdyneProducts", deployment.dependencies.cyberdyneProducts);
  const accessNFT = await ethers.getContractAt("CyberdyneAccessNFT", deployment.dependencies.cyberdyneAccessNFT);

  console.log("\n📋 Contract Addresses:");
  console.log("Marketplace:", deployment.address);
  console.log("USDC Token:", deployment.dependencies.usdcToken);
  console.log("Products:", deployment.dependencies.cyberdyneProducts);
  console.log("AccessNFT:", deployment.dependencies.cyberdyneAccessNFT);

  // Setup demo data
  console.log("\n👥 Setting up demo users...");
  
  // Give marketplace selling permissions to sellers
  await accessNFT.mint(seller1.address, false, false, false, false, false, true, "");
  await accessNFT.mint(seller2.address, false, false, false, false, false, true, "");
  console.log("✅ Minted marketplace access NFTs to sellers");

  // Authorize sellers in products
  await products.authorizeCreator(seller1.address);
  await products.authorizeCreator(seller2.address);
  console.log("✅ Authorized sellers as creators");

  // Create categories
  console.log("\n📂 Creating categories...");
  await products.connect(seller1).createCategory("Hardware", "Computer hardware and electronics");
  await products.connect(seller1).createCategory("Software", "Software tools and applications");
  await products.connect(seller1).createCategory("AI & ML", "Artificial Intelligence and Machine Learning");
  await products.connect(seller1).createCategory("Blockchain", "Blockchain and Web3 development");
  console.log("✅ Created product categories");

  // Create sample products
  console.log("\n🛍️ Creating sample products...");
  const USDC_DECIMALS = 6;
  
  const productTxs = [
    await products.connect(seller1).createProduct(
      "AI-Powered GPU Server", 1, ethers.parseUnits("5000", USDC_DECIMALS), "QmGPUServerIPFS"
    ),
    await products.connect(seller1).createProduct(
      "Quantum Computing SDK", 2, ethers.parseUnits("299", USDC_DECIMALS), "QmQuantumSDKIPFS"
    ),
    await products.connect(seller2).createProduct(
      "Cyberdyne Neural Interface", 1, ethers.parseUnits("15000", USDC_DECIMALS), "QmNeuralInterfaceIPFS"
    ),
    await products.connect(seller2).createProduct(
      "Advanced Encryption Suite", 2, ethers.parseUnits("199", USDC_DECIMALS), "QmEncryptionIPFS"
    ),
    await products.connect(seller1).createProduct(
      "Deep Learning Fundamentals", 3, ethers.parseUnits("149", USDC_DECIMALS), "QmDeepLearningIPFS"
    ),
    await products.connect(seller2).createProduct(
      "Smart Contract Security Guide", 4, ethers.parseUnits("99", USDC_DECIMALS), "QmSecurityIPFS"
    )
  ];

  // Get product UUIDs from transaction receipts
  const productUuids = [];

  for (let tx of productTxs) {
    const receipt = await tx.wait();
    productUuids.push(receipt.logs[0].args.uuid);
  }

  console.log(`✅ Created ${productUuids.length} products`);

  // List some products on marketplace
  console.log("\n🏪 Listing products on marketplace...");
  await marketplace.connect(seller1).listProduct(productUuids[0]); // GPU Server
  await marketplace.connect(seller1).listProduct(productUuids[1]); // Quantum SDK
  await marketplace.connect(seller2).listProduct(productUuids[4]); // Deep Learning
  await marketplace.connect(seller2).listProduct(productUuids[5]); // Security
  console.log("✅ Listed 4 products on marketplace");

  // Setup USDC for buyers
  console.log("\n💰 Setting up USDC for buyers...");
  const buyerAmount = ethers.parseUnits("10000", USDC_DECIMALS); // 10,000 USDC each
  
  await usdcToken.transfer(buyer1.address, buyerAmount);
  await usdcToken.transfer(buyer2.address, buyerAmount);
  
  // Approve marketplace to spend USDC
  await usdcToken.connect(buyer1).approve(deployment.address, buyerAmount);
  await usdcToken.connect(buyer2).approve(deployment.address, buyerAmount);
  console.log("✅ Transferred USDC to buyers and approved marketplace");

  // Display marketplace status
  console.log("\n📊 Marketplace Status:");
  console.log("=====================");
  const activeListings = await marketplace.getAllActiveListings();
  console.log(`Active Listings: ${activeListings.length}`);
  
  for (let i = 0; i < activeListings.length; i++) {
    const listing = activeListings[i];
    const priceFormatted = ethers.formatUnits(listing.priceUSDC, USDC_DECIMALS);
    console.log(`  ${i + 1}. Product - ${priceFormatted} USDC (ID: ${listing.listingId})`);
  }

  console.log(`\nBuyer Balances:`);
  console.log(`  Buyer 1: ${ethers.formatUnits(await usdcToken.balanceOf(buyer1.address), USDC_DECIMALS)} USDC`);
  console.log(`  Buyer 2: ${ethers.formatUnits(await usdcToken.balanceOf(buyer2.address), USDC_DECIMALS)} USDC`);

  // Demonstrate a purchase
  console.log("\n🛒 Demonstrating purchase...");
  const listingToPurchase = activeListings[3]; // Security guide (cheapest)
  console.log(`Buyer 1 purchasing: Listing ID ${listingToPurchase.listingId} for ${ethers.formatUnits(listingToPurchase.priceUSDC, USDC_DECIMALS)} USDC`);
  
  await marketplace.connect(buyer1).purchaseProduct(listingToPurchase.listingId);
  console.log("✅ Purchase completed successfully!");

  // Show updated status
  const updatedListings = await marketplace.getAllActiveListings();
  const buyer1Sales = await marketplace.getBuyerSales(buyer1.address);
  
  console.log(`\nUpdated Marketplace Status:`);
  console.log(`Active Listings: ${updatedListings.length} (was ${activeListings.length})`);
  console.log(`Buyer 1 Purchases: ${buyer1Sales.length}`);
  console.log(`Buyer 1 New Balance: ${ethers.formatUnits(await usdcToken.balanceOf(buyer1.address), USDC_DECIMALS)} USDC`);

  console.log("\n🎉 Demo setup complete!");
  console.log("\n🧪 Testing Commands:");
  console.log("==================");
  console.log("// Connect to marketplace in Hardhat console:");
  console.log(`const marketplace = await ethers.getContractAt("CyberdyneMarketplace", "${deployment.address}");`);
  console.log(`const usdcToken = await ethers.getContractAt("MockERC20", "${deployment.dependencies.usdcToken}");`);
  console.log("\n// Get all active listings:");
  console.log("await marketplace.getAllActiveListings();");
  console.log("\n// Make a purchase (as buyer2):");
  console.log("const [,,,, buyer2] = await ethers.getSigners();");
  console.log("await marketplace.connect(buyer2).purchaseProduct(1); // Use listing ID");
  console.log("\n// Check purchase history:");
  console.log("await marketplace.getBuyerSales(buyer2.address);");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Demo setup failed:", error);
    process.exit(1);
  });