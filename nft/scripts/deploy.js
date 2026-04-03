const hre = require("hardhat");

async function main() {
  console.log("Deploying ReaderEditionNFT to Base...");

  const [deployer] = await hre.ethers.getSigners();
  console.log("Deployer:", deployer.address);

  const NFT = await hre.ethers.getContractFactory("ReaderEditionNFT");
  const nft = await NFT.deploy(deployer.address);

  await nft.waitForDeployment();
  const address = await nft.getAddress();

  console.log("Contract deployed to:", address);
  console.log("Verify with: npx hardhat verify --network base", address);

  // Save deployment address
  const fs = require("fs");
  const deployments = { contract: address, network: "base", timestamp: new Date().toISOString() };
  fs.writeFileSync("./deployments.json", JSON.stringify(deployments, null, 2));
  console.log("Deployment saved to deployments.json");
}

main()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
