const hre = require("hardhat");

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
    "https://api.cyberdyne.xyz/metadata/" // baseURI
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

  // Create some sample NFTs (optional - uncomment if needed)
  /*
  console.log("\nMinting sample access NFTs...");

  const nftTx1 = await cyberdyneAccessNFT.mint(
    deployer.address, // to
    true,  // learningMaterials access
    true,  // frontendServers access
    true,  // backendServers access
    "https://api.cyberdyne.xyz/metadata/admin.json" // custom metadata URI
  );
  const receipt1 = await nftTx1.wait();
  const event1 = receipt1.logs.find(log => log.eventName === "NFTMinted");
  console.log("Minted Admin Access NFT:");
  console.log("  Token ID:", event1.args.tokenId.toString());
  console.log("  To:", event1.args.to);
  console.log("  Learning Access:", event1.args.learningMaterials);
  console.log("  Frontend Access:", event1.args.frontendServers);
  console.log("  Backend Access:", event1.args.backendServers);

  const nftTx2 = await cyberdyneAccessNFT.mint(
    "0x742d35Cc6A0cDB8b5E5A4B5b5e5d2b9a8A5a4B5b", // example address
    true,  // learningMaterials access
    false, // frontendServers access
    false, // backendServers access
    "https://api.cyberdyne.xyz/metadata/student.json" // custom metadata URI
  );
  const receipt2 = await nftTx2.wait();
  const event2 = receipt2.logs.find(log => log.eventName === "NFTMinted");
  console.log("Minted Student Access NFT:");
  console.log("  Token ID:", event2.args.tokenId.toString());
  console.log("  To:", event2.args.to);
  console.log("  Learning Access:", event2.args.learningMaterials);
  console.log("  Frontend Access:", event2.args.frontendServers);
  console.log("  Backend Access:", event2.args.backendServers);

  const nftTx3 = await cyberdyneAccessNFT.mint(
    "0x123d35Cc6A0cDB8b5E5A4B5b5e5d2b9a8A5a4B5c", // example address
    false, // learningMaterials access
    true,  // frontendServers access
    true,  // backendServers access
    "https://api.cyberdyne.xyz/metadata/developer.json" // custom metadata URI
  );
  const receipt3 = await nftTx3.wait();
  const event3 = receipt3.logs.find(log => log.eventName === "NFTMinted");
  console.log("Minted Developer Access NFT:");
  console.log("  Token ID:", event3.args.tokenId.toString());
  console.log("  To:", event3.args.to);
  console.log("  Learning Access:", event3.args.learningMaterials);
  console.log("  Frontend Access:", event3.args.frontendServers);
  console.log("  Backend Access:", event3.args.backendServers);

  // Display final state
  const finalTotalSupply = await cyberdyneAccessNFT.totalSupply();
  console.log("\nFinal state:");
  console.log("Final totalSupply:", finalTotalSupply.toString());

  // Test permission checking
  console.log("\nTesting access permissions:");
  const token1Permissions = await cyberdyneAccessNFT.getTokenPermissions(1);
  console.log("Token 1 permissions:", {
    learningMaterials: token1Permissions.learningMaterials,
    frontendServers: token1Permissions.frontendServers,
    backendServers: token1Permissions.backendServers,
    issuedAt: new Date(Number(token1Permissions.issuedAt) * 1000).toISOString(),
    metadataURI: token1Permissions.metadataURI
  });

  // Test address-based access checking
  const deployerHasLearning = await cyberdyneAccessNFT.addressHasLearningAccess(deployer.address);
  const deployerHasFrontend = await cyberdyneAccessNFT.addressHasFrontendAccess(deployer.address);
  const deployerHasBackend = await cyberdyneAccessNFT.addressHasBackendAccess(deployer.address);
  console.log(`Deployer access - Learning: ${deployerHasLearning}, Frontend: ${deployerHasFrontend}, Backend: ${deployerHasBackend}`);
  */

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
  console.log("5. Check access using hasLearningAccess, hasFrontendAccess, hasBackendAccess");
  console.log("6. Query user tokens using getUserTokens and getUserPermissions");
  console.log("7. Update metadata using updateMetadata function (authorized managers)");
  console.log("8. Transfer contract ownership using transferContractOwnership (owner only)");

  // Save deployment info to a file
  const fs = require('fs');
  
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
    baseURI: "https://api.cyberdyne.xyz/metadata/",
    deploymentTime: new Date().toISOString(),
    blockNumber: await hre.ethers.provider.getBlockNumber()
  };

  fs.writeFileSync(
    `deployments/CyberdyneAccessNFT-${hre.network.name}.json`,
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log(`\n💾 Deployment info saved to deployments/CyberdyneAccessNFT-${hre.network.name}.json`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:");
    console.error(error);
    process.exit(1);
  });