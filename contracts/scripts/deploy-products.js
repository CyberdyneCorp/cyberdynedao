import hre from "hardhat";
import fs from 'fs';

async function main() {
  console.log("Starting CyberdyneProducts contract deployment...");

  // Get the deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(await hre.ethers.provider.getBalance(deployer.address)));

  // Deploy the contract
  const CyberdyneProducts = await hre.ethers.getContractFactory("CyberdyneProducts");
  console.log("Deploying CyberdyneProducts contract...");
  
  const cyberdyneProducts = await CyberdyneProducts.deploy();
  await cyberdyneProducts.waitForDeployment();

  const contractAddress = await cyberdyneProducts.getAddress();
  console.log("CyberdyneProducts contract deployed to:", contractAddress);

  // Verify the owner
  const owner = await cyberdyneProducts.owner();
  console.log("Contract owner:", owner);
  console.log("Deployer address:", deployer.address);
  console.log("Owner matches deployer:", owner === deployer.address);

  // Display initial state
  const totalProducts = await cyberdyneProducts.getTotalProductCount();
  console.log("Initial totalProducts:", totalProducts.toString());
  
  // Display authorization info
  const authorizedCreators = await cyberdyneProducts.getAuthorizedCreators();
  console.log("Authorized creators:", authorizedCreators);

  // Create some sample products (optional - uncomment if needed)
  /*
  console.log("\nCreating sample products...");

  const productTx1 = await cyberdyneProducts.createProduct(
    "Trade4Me Pro",
    hre.ethers.parseUnits("99.99", 6), // 99.99 USDC (6 decimals)
    "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdA" // Sample IPFS hash
  );
  const receipt1 = await productTx1.wait();
  const event1 = receipt1.logs.find(log => log.eventName === "ProductCreated");
  console.log("Created product: Trade4Me Pro");
  console.log("  UUID:", event1.args.uuid);
  console.log("  Price:", hre.ethers.formatUnits(event1.args.priceUSDC, 6), "USDC");
  console.log("  Creator:", event1.args.creator);

  const productTx2 = await cyberdyneProducts.createProduct(
    "Liquidity4Me Premium",
    hre.ethers.parseUnits("149.99", 6), // 149.99 USDC (6 decimals)
    "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdB" // Sample IPFS hash
  );
  const receipt2 = await productTx2.wait();
  const event2 = receipt2.logs.find(log => log.eventName === "ProductCreated");
  console.log("Created product: Liquidity4Me Premium");
  console.log("  UUID:", event2.args.uuid);
  console.log("  Price:", hre.ethers.formatUnits(event2.args.priceUSDC, 6), "USDC");
  console.log("  Creator:", event2.args.creator);

  const productTx3 = await cyberdyneProducts.createProduct(
    "Surf4Me Analytics",
    hre.ethers.parseUnits("79.99", 6), // 79.99 USDC (6 decimals)
    "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdC" // Sample IPFS hash
  );
  const receipt3 = await productTx3.wait();
  const event3 = receipt3.logs.find(log => log.eventName === "ProductCreated");
  console.log("Created product: Surf4Me Analytics");
  console.log("  UUID:", event3.args.uuid);
  console.log("  Price:", hre.ethers.formatUnits(event3.args.priceUSDC, 6), "USDC");
  console.log("  Creator:", event3.args.creator);

  const productTx4 = await cyberdyneProducts.createProduct(
    "bHealthy Tracker",
    hre.ethers.parseUnits("29.99", 6), // 29.99 USDC (6 decimals)
    "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdD" // Sample IPFS hash
  );
  const receipt4 = await productTx4.wait();
  const event4 = receipt4.logs.find(log => log.eventName === "ProductCreated");
  console.log("Created product: bHealthy Tracker");
  console.log("  UUID:", event4.args.uuid);
  console.log("  Price:", hre.ethers.formatUnits(event4.args.priceUSDC, 6), "USDC");
  console.log("  Creator:", event4.args.creator);

  // Display final state
  const finalTotalProducts = await cyberdyneProducts.totalProducts();
  const activeProductCount = await cyberdyneProducts.getActiveProductCount();
  console.log("\nFinal state:");
  console.log("Final totalProducts:", finalTotalProducts.toString());
  console.log("Active products:", activeProductCount.toString());
  */

  console.log("\n✅ Deployment completed successfully!");
  console.log("\n📋 Contract Details:");
  console.log("====================");
  console.log("Contract Address:", contractAddress);
  console.log("Network:", hre.network.name);
  console.log("Owner:", owner);
  console.log("\n📚 Next Steps:");
  console.log("1. Verify the contract on Etherscan (if deploying to mainnet/testnet)");
  console.log("2. Authorize additional creators using authorizeCreator function (owner only)");
  console.log("3. Create products using the createProduct function (authorized creators only)");
  console.log("4. Query products by creator using getAllProductsByCreator or getProductsByCreator (paginated)");
  console.log("5. Update products using updateProduct (owner or creator only)");
  console.log("6. Toggle product status using toggleProductStatus (owner or creator only)");
  console.log("7. Delete products using deleteProduct (owner or creator only)");
  console.log("8. Transfer contract ownership using transferContractOwnership (owner only)");

  // Save deployment info to a file
  
  // Ensure deployments directory exists
  if (!fs.existsSync('deployments')) {
    fs.mkdirSync('deployments');
  }
  
  const deploymentInfo = {
    contractAddress: contractAddress,
    network: hre.network.name,
    deployer: deployer.address,
    owner: owner,
    deploymentTime: new Date().toISOString(),
    blockNumber: await hre.ethers.provider.getBlockNumber()
  };

  fs.writeFileSync(
    `deployments/CyberdyneProducts-${hre.network.name}.json`,
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log(`\n💾 Deployment info saved to deployments/CyberdyneProducts-${hre.network.name}.json`);

  // Auto-verify on testnets and mainnet (not local)
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("\n🔍 Starting automatic contract verification...");
    try {
      await hre.run("verify:verify", {
        address: contractAddress,
        constructorArguments: [],
      });
      console.log("✅ Contract verified successfully on BaseScan!");
      console.log(`🔗 View on BaseScan: https://basescan.org/address/${contractAddress}`);
    } catch (error) {
      console.log("⚠️ Verification failed (this is normal if already verified):");
      console.log(error.message);
      console.log(`\n🔧 Manual verification command:`);
      console.log(`npx hardhat verify --network ${hre.network.name} ${contractAddress}`);
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:");
    console.error(error);
    process.exit(1);
  });