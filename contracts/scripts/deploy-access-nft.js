import hre from "hardhat";
import fs from 'fs';

async function main() {
  console.log("Starting CyberdyneAccessNFT contract deployment...");

  // Get the deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(await hre.ethers.provider.getBalance(deployer.address)));

  // Deploy the contract
  const CyberdyneAccessNFT = await hre.ethers.getContractFactory("CyberdyneAccessNFT");
  console.log("Deploying CyberdyneAccessNFT contract...");
  
  const cyberdyneAccessNFT = await CyberdyneAccessNFT.deploy(
    "Cyberdyne Access Pass", // name
    "CYBACC", // symbol
    "https://apigateway.coolify.cyberdynecorp.ai/" // baseURI
  );
  await cyberdyneAccessNFT.waitForDeployment();

  const contractAddress = await cyberdyneAccessNFT.getAddress();
  console.log("CyberdyneAccessNFT contract deployed to:", contractAddress);

  // Verify the owner
  const owner = await cyberdyneAccessNFT.owner();
  console.log("Contract owner:", owner);
  console.log("Deployer address:", deployer.address);
  console.log("Owner matches deployer:", owner === deployer.address);

  // Display initial state
  const totalSupply = await cyberdyneAccessNFT.totalSupply();
  const nextTokenId = await cyberdyneAccessNFT.getNextTokenId();
  console.log("Initial totalSupply:", totalSupply.toString());
  console.log("Next token ID:", nextTokenId.toString());
  
  // Display authorization info
  const authorizedManagers = await cyberdyneAccessNFT.getAuthorizedManagers();
  console.log("Authorized managers:", authorizedManagers);

  console.log("\n✅ Deployment completed successfully!");
  console.log("\n📋 Contract Details:");
  console.log("====================");
  console.log("Contract Address:", contractAddress);
  console.log("Network:", hre.network.name);
  console.log("Owner:", owner);
  console.log("NFT Name: Cyberdyne Access Pass");
  console.log("NFT Symbol: CYBACC");
  console.log("\n📚 Next Steps:");
  console.log("1. Verify the contract on Etherscan (if deploying to mainnet/testnet)");
  console.log("2. Authorize additional managers using authorizeManager function (owner only)");
  console.log("3. Mint access NFTs using the mint function (owner only)");
  console.log("4. Update permissions using updatePermissions function (authorized managers)");
  console.log("5. Check access using hasLearningAccess, hasFrontendAccess, hasBackendAccess, hasBlogCreatorAccess, hasAdminAccess, hasMarketplaceSellAccess");
  console.log("6. Query user tokens using getUserTokens and getUserPermissions");
  console.log("7. Update metadata using updateMetadata function (authorized managers)");
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
    nftName: "Cyberdyne Access Pass",
    nftSymbol: "CYBACC",
    baseURI: "https://apigateway.coolify.cyberdynecorp.ai/",
    deploymentTime: new Date().toISOString(),
    blockNumber: await hre.ethers.provider.getBlockNumber()
  };

  fs.writeFileSync(
    `deployments/CyberdyneAccessNFT-${hre.network.name}.json`,
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log(`\n💾 Deployment info saved to deployments/CyberdyneAccessNFT-${hre.network.name}.json`);

  // Auto-verify on testnets and mainnet (not local)
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("\n🔍 Starting automatic contract verification...");
    try {
      await hre.run("verify:verify", {
        address: contractAddress,
        constructorArguments: [
          "Cyberdyne Access Pass",
          "CYBACC", 
          "https://apigateway.coolify.cyberdynecorp.ai/"
        ],
      });
      console.log("✅ Contract verified successfully on BaseScan!");
      console.log(`🔗 View on BaseScan: https://basescan.org/address/${contractAddress}`);
    } catch (error) {
      console.log("⚠️ Verification failed (this is normal if already verified):");
      console.log(error.message);
      console.log(`\n🔧 Manual verification command:`);
      console.log(`npx hardhat verify --network ${hre.network.name} ${contractAddress} "Cyberdyne Access Pass" "CYBACC" "https://apigateway.coolify.cyberdynecorp.ai/"`);
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