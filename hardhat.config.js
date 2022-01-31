require('@nomiclabs/hardhat-etherscan');
require('@nomiclabs/hardhat-ethers');
require('@nomiclabs/hardhat-waffle');
require("@nomiclabs/hardhat-truffle5");
require("@nomiclabs/hardhat-ganache");
require('hardhat-deploy');
require('hardhat-deploy-ethers');
require('hardhat-tracer');
require("dotenv").config();

const PRIVATE_KEY = process.env.PRIVATE_KEY;
const ANOTHER_PRIVATE_KEY = process.env.ANOTHER_PRIVATE_KEY;
const FTM_KEY = process.env.FTM_KEY;
if (!process.env.PRIVATE_KEY) {
  throw new Error("ENV Variable PRIVATE_KEY not set!");
}
if (!process.env.ANOTHER_PRIVATE_KEY) {
  throw new Error("ENV Variable ANOTHER_PRIVATE_KEY not set!");
}
if (!process.env.FTM_KEY) {
  throw new Error("ENV Variable FTM_KEY not set!");
}

module.exports = {
    solidity: {
        version: '0.8.10',
        settings: {
          optimizer: {
            enabled: true,
            runs: 200,
          },
          outputSelection: {
            "*": {
              "*": ["storageLayout"]
            }
          }
        }
    },
    networks: {
        hardhat: {
            forking: {
                url: "http://localhost:8545",
                // url: 'https://rpc.ftm.tools',
                blockNumber: 28455130,
            },
            timeout: 2000000000,
            chainId: 250
        },
        localhost: {
          url: "http://localhost:8545",
          timeout: 2000000000,
          accounts: [PRIVATE_KEY, ANOTHER_PRIVATE_KEY]
        },
        fantom: {
          chainId: 250,
          url: 'https://rpc.ftm.tools',
          accounts: [PRIVATE_KEY, ANOTHER_PRIVATE_KEY]
        }
    },
    namedAccounts: {
        deployer: {
            default: 0,
        },
    },
    etherscan: {
      apiKey: FTM_KEY
    }
};