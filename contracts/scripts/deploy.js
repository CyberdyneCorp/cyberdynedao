const hre = require("hardhat");

async function main() {
  console.log("Starting TrainingMaterials contract deployment...");

  // Get the deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(await hre.ethers.provider.getBalance(deployer.address)));

  // Deploy the contract
  const TrainingMaterials = await hre.ethers.getContractFactory("TrainingMaterials");
  console.log("Deploying TrainingMaterials contract...");
  
  const trainingMaterials = await TrainingMaterials.deploy();
  await trainingMaterials.waitForDeployment();

  const contractAddress = await trainingMaterials.getAddress();
  console.log("TrainingMaterials contract deployed to:", contractAddress);

  // Verify the owner
  const owner = await trainingMaterials.owner();
  console.log("Contract owner:", owner);
  console.log("Deployer address:", deployer.address);
  console.log("Owner matches deployer:", owner === deployer.address);

  // Display initial state
  const nextCategoryId = await trainingMaterials.nextCategoryId();
  const totalMaterials = await trainingMaterials.totalMaterials();
  console.log("Initial nextCategoryId:", nextCategoryId.toString());
  console.log("Initial totalMaterials:", totalMaterials.toString());
  
  // Display authorization info
  const authorizedCreatorsCount = await trainingMaterials.getAuthorizedCreatorsCount();
  const authorizedCreators = await trainingMaterials.getAuthorizedCreators();
  console.log("Authorized creators count:", authorizedCreatorsCount.toString());
  console.log("Authorized creators:", authorizedCreators);

  // Create some sample data (optional - uncomment if needed)
  /*
  console.log("\nCreating sample categories...");
  
  const tx1 = await trainingMaterials.createCategory(
    "Blockchain Fundamentals",
    "Learn the basics of blockchain technology and its applications"
  );
  await tx1.wait();
  console.log("Created category: Blockchain Fundamentals");

  const tx2 = await trainingMaterials.createCategory(
    "Smart Contract Development",
    "Advanced topics on developing and deploying smart contracts"
  );
  await tx2.wait();
  console.log("Created category: Smart Contract Development");

  const tx3 = await trainingMaterials.createCategory(
    "DeFi Protocols",
    "Understanding decentralized finance protocols and mechanisms"
  );
  await tx3.wait();
  console.log("Created category: DeFi Protocols");

  console.log("\nCreating sample training materials...");

  const materialTx1 = await trainingMaterials.createTrainingMaterial(
    "Introduction to Blockchain",
    "A comprehensive introduction to blockchain technology covering consensus mechanisms, cryptography, and distributed systems.",
    1, // Blockchain Fundamentals category
    "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG", // Sample IPFS hash for image
    "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdH", // Sample IPFS hash for content
    "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdK", // Sample IPFS hash for context file
    hre.ethers.parseUnits("19.99", 6) // 19.99 USDC
  );
  const receipt1 = await materialTx1.wait();
  const event1 = receipt1.logs.find(log => log.eventName === "TrainingMaterialCreated");
  console.log("Created material: Introduction to Blockchain");
  console.log("  UUID:", event1.args.uuid);
  console.log("  Price:", hre.ethers.formatUnits(event1.args.priceUSDC, 6), "USDC");
  console.log("  Creator:", event1.args.creator);

  const materialTx2 = await trainingMaterials.createTrainingMaterial(
    "Solidity Programming",
    "Learn Solidity programming language from basics to advanced concepts including best practices and security considerations.",
    2, // Smart Contract Development category
    "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdI", // Sample IPFS hash for image
    "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdJ", // Sample IPFS hash for content
    "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdL", // Sample IPFS hash for context file
    hre.ethers.parseUnits("49.99", 6) // 49.99 USDC
  );
  const receipt2 = await materialTx2.wait();
  const event2 = receipt2.logs.find(log => log.eventName === "TrainingMaterialCreated");
  console.log("Created material: Solidity Programming");
  console.log("  UUID:", event2.args.uuid);
  console.log("  Price:", hre.ethers.formatUnits(event2.args.priceUSDC, 6), "USDC");
  console.log("  Creator:", event2.args.creator);

  // Display final state
  const finalNextCategoryId = await trainingMaterials.nextCategoryId();
  const finalTotalMaterials = await trainingMaterials.totalMaterials();
  console.log("\nFinal state:");
  console.log("Final nextCategoryId:", finalNextCategoryId.toString());
  console.log("Final totalMaterials:", finalTotalMaterials.toString());
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
  console.log("3. Create categories using the createCategory function (owner only)");
  console.log("4. Add training materials using the createTrainingMaterial function (authorized creators only)");
  console.log("5. Query materials by category using getTrainingMaterialsByCategory");
  console.log("6. Query materials by creator using getTrainingMaterialsByCreator");
  console.log("7. Delete materials using deleteTrainingMaterial (owner or creator only)");
  console.log("8. Transfer contract ownership using transferContractOwnership (owner only)");

  // Save deployment info to a file
  const fs = require('fs');
  const deploymentInfo = {
    contractAddress: contractAddress,
    network: hre.network.name,
    deployer: deployer.address,
    owner: owner,
    deploymentTime: new Date().toISOString(),
    blockNumber: await hre.ethers.provider.getBlockNumber()
  };

  fs.writeFileSync(
    `deployments/TrainingMaterials-${hre.network.name}.json`,
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log(`\n💾 Deployment info saved to deployments/TrainingMaterials-${hre.network.name}.json`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:");
    console.error(error);
    process.exit(1);
  });