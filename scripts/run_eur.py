import pytest
from brownie import MetaVault, VaultSwapper, Contract, Wei, accounts, chain, convert

PATH_EURS_TO_EURT = [[1, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0], [0, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 1, 0]]
PATH_EURS_TO_IBEUR = [[1, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0], [0, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0]]
PATH_EURS_TO_EURN = [[1, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 0, 0], [2, "0x3CFAa1596777CAD9f5004F9a0c443d912E262243", 2, 1], [0, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0]]
PATH_EURS_TO_3EUR = [[1, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 0, 0], [0, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 2, 0]]

PATH_EURT_TO_EURS = [[1, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 1, 0], [0, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0]]
PATH_EURT_TO_IBEUR = [[1, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 1, 0], [0, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0]]
PATH_EURT_TO_EURN = [[1, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 0], [0, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0]]
PATH_EURT_TO_3EUR = [[1, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 0], [0, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 1, 0]]

PATH_IBEUR_TO_EURS = [[1, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0], [0, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0]]
PATH_IBEUR_TO_EURT = [[1, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0], [0, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 1, 0]]
PATH_IBEUR_TO_EURN = [[1, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0], [2, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 1, 0], [0, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0]]
PATH_IBEUR_TO_3EUR = [[1, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 0, 0], [2, "0xB37D6c07482Bc11cd28a1f11f1a6ad7b66Dec933", 0, 1], [0, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 0, 0]]

PATH_EURN_TO_EURS = [[1, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0], [2, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 1], [0, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0]]
PATH_EURN_TO_EURT = [[1, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0], [0, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 0]]
PATH_EURN_TO_IBEUR = [[1, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0], [2, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 1], [0, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0]]
PATH_EURN_TO_3EUR = [[1, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0], [0, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 1, 0]]

PATH_3EUR_TO_EURS = [[1, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 2, 0], [0, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 0, 0]]
PATH_3EUR_TO_EURT = [[1, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 1, 0], [0, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 0]]
PATH_3EUR_TO_IBEUR = [[1, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 0, 0], [2, "0x45a8CC73EC100306af64AB2CcB7B12E70EC549A8", 0, 1], [0, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0]]
PATH_3EUR_TO_EURN = [[1, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 1, 0], [0, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0]]


VAULT_ABI = [{"name":"Transfer","inputs":[{"name":"sender","type":"address","indexed":True},{"name":"receiver","type":"address","indexed":True},{"name":"value","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"Approval","inputs":[{"name":"owner","type":"address","indexed":True},{"name":"spender","type":"address","indexed":True},{"name":"value","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"StrategyAdded","inputs":[{"name":"strategy","type":"address","indexed":True},{"name":"debtRatio","type":"uint256","indexed":False},{"name":"minDebtPerHarvest","type":"uint256","indexed":False},{"name":"maxDebtPerHarvest","type":"uint256","indexed":False},{"name":"performanceFee","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"StrategyReported","inputs":[{"name":"strategy","type":"address","indexed":True},{"name":"gain","type":"uint256","indexed":False},{"name":"loss","type":"uint256","indexed":False},{"name":"debtPaid","type":"uint256","indexed":False},{"name":"totalGain","type":"uint256","indexed":False},{"name":"totalLoss","type":"uint256","indexed":False},{"name":"totalDebt","type":"uint256","indexed":False},{"name":"debtAdded","type":"uint256","indexed":False},{"name":"debtRatio","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"UpdateGovernance","inputs":[{"name":"governance","type":"address","indexed":False}],"anonymous":False,"type":"event"},{"name":"UpdateManagement","inputs":[{"name":"management","type":"address","indexed":False}],"anonymous":False,"type":"event"},{"name":"UpdateGuestList","inputs":[{"name":"guestList","type":"address","indexed":False}],"anonymous":False,"type":"event"},{"name":"UpdateRewards","inputs":[{"name":"rewards","type":"address","indexed":False}],"anonymous":False,"type":"event"},{"name":"UpdateDepositLimit","inputs":[{"name":"depositLimit","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"UpdatePerformanceFee","inputs":[{"name":"performanceFee","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"UpdateManagementFee","inputs":[{"name":"managementFee","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"UpdateGuardian","inputs":[{"name":"guardian","type":"address","indexed":False}],"anonymous":False,"type":"event"},{"name":"EmergencyShutdown","inputs":[{"name":"active","type":"bool","indexed":False}],"anonymous":False,"type":"event"},{"name":"UpdateWithdrawalQueue","inputs":[{"name":"queue","type":"address[20]","indexed":False}],"anonymous":False,"type":"event"},{"name":"StrategyUpdateDebtRatio","inputs":[{"name":"strategy","type":"address","indexed":True},{"name":"debtRatio","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"StrategyUpdateMinDebtPerHarvest","inputs":[{"name":"strategy","type":"address","indexed":True},{"name":"minDebtPerHarvest","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"StrategyUpdateMaxDebtPerHarvest","inputs":[{"name":"strategy","type":"address","indexed":True},{"name":"maxDebtPerHarvest","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"StrategyUpdatePerformanceFee","inputs":[{"name":"strategy","type":"address","indexed":True},{"name":"performanceFee","type":"uint256","indexed":False}],"anonymous":False,"type":"event"},{"name":"StrategyMigrated","inputs":[{"name":"oldVersion","type":"address","indexed":True},{"name":"newVersion","type":"address","indexed":True}],"anonymous":False,"type":"event"},{"name":"StrategyRevoked","inputs":[{"name":"strategy","type":"address","indexed":True}],"anonymous":False,"type":"event"},{"name":"StrategyRemovedFromQueue","inputs":[{"name":"strategy","type":"address","indexed":True}],"anonymous":False,"type":"event"},{"name":"StrategyAddedToQueue","inputs":[{"name":"strategy","type":"address","indexed":True}],"anonymous":False,"type":"event"},{"stateMutability":"nonpayable","type":"function","name":"initialize","inputs":[{"name":"token","type":"address"},{"name":"governance","type":"address"},{"name":"rewards","type":"address"},{"name":"nameOverride","type":"string"},{"name":"symbolOverride","type":"string"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"initialize","inputs":[{"name":"token","type":"address"},{"name":"governance","type":"address"},{"name":"rewards","type":"address"},{"name":"nameOverride","type":"string"},{"name":"symbolOverride","type":"string"},{"name":"guardian","type":"address"}],"outputs":[]},{"stateMutability":"pure","type":"function","name":"apiVersion","inputs":[],"outputs":[{"name":"","type":"string"}],"gas":4546},{"stateMutability":"nonpayable","type":"function","name":"setName","inputs":[{"name":"name","type":"string"}],"outputs":[],"gas":107044},{"stateMutability":"nonpayable","type":"function","name":"setSymbol","inputs":[{"name":"symbol","type":"string"}],"outputs":[],"gas":71894},{"stateMutability":"nonpayable","type":"function","name":"setGovernance","inputs":[{"name":"governance","type":"address"}],"outputs":[],"gas":36365},{"stateMutability":"nonpayable","type":"function","name":"acceptGovernance","inputs":[],"outputs":[],"gas":37637},{"stateMutability":"nonpayable","type":"function","name":"setManagement","inputs":[{"name":"management","type":"address"}],"outputs":[],"gas":37775},{"stateMutability":"nonpayable","type":"function","name":"setGuestList","inputs":[{"name":"guestList","type":"address"}],"outputs":[],"gas":37805},{"stateMutability":"nonpayable","type":"function","name":"setRewards","inputs":[{"name":"rewards","type":"address"}],"outputs":[],"gas":37835},{"stateMutability":"nonpayable","type":"function","name":"setLockedProfitDegration","inputs":[{"name":"degration","type":"uint256"}],"outputs":[],"gas":36519},{"stateMutability":"nonpayable","type":"function","name":"setDepositLimit","inputs":[{"name":"limit","type":"uint256"}],"outputs":[],"gas":37795},{"stateMutability":"nonpayable","type":"function","name":"setPerformanceFee","inputs":[{"name":"fee","type":"uint256"}],"outputs":[],"gas":37929},{"stateMutability":"nonpayable","type":"function","name":"setManagementFee","inputs":[{"name":"fee","type":"uint256"}],"outputs":[],"gas":37959},{"stateMutability":"nonpayable","type":"function","name":"setGuardian","inputs":[{"name":"guardian","type":"address"}],"outputs":[],"gas":39203},{"stateMutability":"nonpayable","type":"function","name":"setEmergencyShutdown","inputs":[{"name":"active","type":"bool"}],"outputs":[],"gas":39274},{"stateMutability":"nonpayable","type":"function","name":"setWithdrawalQueue","inputs":[{"name":"queue","type":"address[20]"}],"outputs":[],"gas":763950},{"stateMutability":"nonpayable","type":"function","name":"transfer","inputs":[{"name":"receiver","type":"address"},{"name":"amount","type":"uint256"}],"outputs":[{"name":"","type":"bool"}],"gas":76768},{"stateMutability":"nonpayable","type":"function","name":"transferFrom","inputs":[{"name":"sender","type":"address"},{"name":"receiver","type":"address"},{"name":"amount","type":"uint256"}],"outputs":[{"name":"","type":"bool"}],"gas":116531},{"stateMutability":"nonpayable","type":"function","name":"approve","inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"outputs":[{"name":"","type":"bool"}],"gas":38271},{"stateMutability":"nonpayable","type":"function","name":"increaseAllowance","inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"outputs":[{"name":"","type":"bool"}],"gas":40312},{"stateMutability":"nonpayable","type":"function","name":"decreaseAllowance","inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"outputs":[{"name":"","type":"bool"}],"gas":40336},{"stateMutability":"nonpayable","type":"function","name":"permit","inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"},{"name":"amount","type":"uint256"},{"name":"expiry","type":"uint256"},{"name":"signature","type":"bytes"}],"outputs":[{"name":"","type":"bool"}],"gas":81264},{"stateMutability":"view","type":"function","name":"totalAssets","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":4098},{"stateMutability":"nonpayable","type":"function","name":"deposit","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"deposit","inputs":[{"name":"_amount","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"deposit","inputs":[{"name":"_amount","type":"uint256"},{"name":"recipient","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"maxAvailableShares","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":383839},{"stateMutability":"nonpayable","type":"function","name":"withdraw","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"withdraw","inputs":[{"name":"maxShares","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"withdraw","inputs":[{"name":"maxShares","type":"uint256"},{"name":"recipient","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"withdraw","inputs":[{"name":"maxShares","type":"uint256"},{"name":"recipient","type":"address"},{"name":"maxLoss","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"pricePerShare","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":18195},{"stateMutability":"nonpayable","type":"function","name":"addStrategy","inputs":[{"name":"strategy","type":"address"},{"name":"debtRatio","type":"uint256"},{"name":"minDebtPerHarvest","type":"uint256"},{"name":"maxDebtPerHarvest","type":"uint256"},{"name":"performanceFee","type":"uint256"}],"outputs":[],"gas":1485796},{"stateMutability":"nonpayable","type":"function","name":"updateStrategyDebtRatio","inputs":[{"name":"strategy","type":"address"},{"name":"debtRatio","type":"uint256"}],"outputs":[],"gas":115193},{"stateMutability":"nonpayable","type":"function","name":"updateStrategyMinDebtPerHarvest","inputs":[{"name":"strategy","type":"address"},{"name":"minDebtPerHarvest","type":"uint256"}],"outputs":[],"gas":42441},{"stateMutability":"nonpayable","type":"function","name":"updateStrategyMaxDebtPerHarvest","inputs":[{"name":"strategy","type":"address"},{"name":"maxDebtPerHarvest","type":"uint256"}],"outputs":[],"gas":42471},{"stateMutability":"nonpayable","type":"function","name":"updateStrategyPerformanceFee","inputs":[{"name":"strategy","type":"address"},{"name":"performanceFee","type":"uint256"}],"outputs":[],"gas":41251},{"stateMutability":"nonpayable","type":"function","name":"migrateStrategy","inputs":[{"name":"oldVersion","type":"address"},{"name":"newVersion","type":"address"}],"outputs":[],"gas":1141468},{"stateMutability":"nonpayable","type":"function","name":"revokeStrategy","inputs":[],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"revokeStrategy","inputs":[{"name":"strategy","type":"address"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"addStrategyToQueue","inputs":[{"name":"strategy","type":"address"}],"outputs":[],"gas":1199804},{"stateMutability":"nonpayable","type":"function","name":"removeStrategyFromQueue","inputs":[{"name":"strategy","type":"address"}],"outputs":[],"gas":23088703},{"stateMutability":"view","type":"function","name":"debtOutstanding","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"debtOutstanding","inputs":[{"name":"strategy","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"creditAvailable","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"creditAvailable","inputs":[{"name":"strategy","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"availableDepositLimit","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":9551},{"stateMutability":"view","type":"function","name":"expectedReturn","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"expectedReturn","inputs":[{"name":"strategy","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"report","inputs":[{"name":"gain","type":"uint256"},{"name":"loss","type":"uint256"},{"name":"_debtPayment","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}],"gas":1015170},{"stateMutability":"nonpayable","type":"function","name":"sweep","inputs":[{"name":"token","type":"address"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"sweep","inputs":[{"name":"token","type":"address"},{"name":"amount","type":"uint256"}],"outputs":[]},{"stateMutability":"view","type":"function","name":"name","inputs":[],"outputs":[{"name":"","type":"string"}],"gas":8750},{"stateMutability":"view","type":"function","name":"symbol","inputs":[],"outputs":[{"name":"","type":"string"}],"gas":7803},{"stateMutability":"view","type":"function","name":"decimals","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2408},{"stateMutability":"view","type":"function","name":"precisionFactor","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2438},{"stateMutability":"view","type":"function","name":"balanceOf","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":2683},{"stateMutability":"view","type":"function","name":"allowance","inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":2928},{"stateMutability":"view","type":"function","name":"totalSupply","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2528},{"stateMutability":"view","type":"function","name":"token","inputs":[],"outputs":[{"name":"","type":"address"}],"gas":2558},{"stateMutability":"view","type":"function","name":"governance","inputs":[],"outputs":[{"name":"","type":"address"}],"gas":2588},{"stateMutability":"view","type":"function","name":"management","inputs":[],"outputs":[{"name":"","type":"address"}],"gas":2618},{"stateMutability":"view","type":"function","name":"guardian","inputs":[],"outputs":[{"name":"","type":"address"}],"gas":2648},{"stateMutability":"view","type":"function","name":"guestList","inputs":[],"outputs":[{"name":"","type":"address"}],"gas":2678},{"stateMutability":"view","type":"function","name":"strategies","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"performanceFee","type":"uint256"},{"name":"activation","type":"uint256"},{"name":"debtRatio","type":"uint256"},{"name":"minDebtPerHarvest","type":"uint256"},{"name":"maxDebtPerHarvest","type":"uint256"},{"name":"lastReport","type":"uint256"},{"name":"totalDebt","type":"uint256"},{"name":"totalGain","type":"uint256"},{"name":"totalLoss","type":"uint256"}],"gas":11031},{"stateMutability":"view","type":"function","name":"withdrawalQueue","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}],"gas":2847},{"stateMutability":"view","type":"function","name":"emergencyShutdown","inputs":[],"outputs":[{"name":"","type":"bool"}],"gas":2768},{"stateMutability":"view","type":"function","name":"depositLimit","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2798},{"stateMutability":"view","type":"function","name":"debtRatio","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2828},{"stateMutability":"view","type":"function","name":"totalDebt","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2858},{"stateMutability":"view","type":"function","name":"lastReport","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2888},{"stateMutability":"view","type":"function","name":"activation","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2918},{"stateMutability":"view","type":"function","name":"lockedProfit","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2948},{"stateMutability":"view","type":"function","name":"lockedProfitDegration","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2978},{"stateMutability":"view","type":"function","name":"rewards","inputs":[],"outputs":[{"name":"","type":"address"}],"gas":3008},{"stateMutability":"view","type":"function","name":"managementFee","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":3038},{"stateMutability":"view","type":"function","name":"performanceFee","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":3068},{"stateMutability":"view","type":"function","name":"nonces","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":3313},{"stateMutability":"view","type":"function","name":"DOMAIN_SEPARATOR","inputs":[],"outputs":[{"name":"","type":"bytes32"}],"gas":3128}]

curveEURSToken = "0x194eBd173F6cDacE046C53eACcE9B953F28411d1"
curveEURSTokenWhale = "0x90bb609649e0451e5ad952683d64bd2d1f245840"
curveEURSVault = "0x25212Df29073FfFA7A67399AcEfC2dd75a831A1A"

curveEURTToken = "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890"
curveEURTTokenWhale = "0xe8060ad8971450e624d5289a10017dd30f5da85f"
curveEURTVault = "0x0d4EA8536F9A13e4FBa16042a46c30f092b06aA5"

curveibEURToken = "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859"
curveibEURVault = "0x67e019bfbd5a67207755D04467D6A70c0B75bF60"

curveEURNToken = "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a"
curveEURNVault = "0x8b9C0c24307344B6D7941ab654b2Aeee25347473"

curve3EURToken = "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571"
curve3EURVault = "0x5AB64C599FcC59f0f2726A300b03166A395578Da"

deployer = accounts[0]
depositor = accounts[1]
another_depositor = accounts[2]
third_depositor = accounts[3]
bowswap = deployer.deploy(VaultSwapper)
bowswap.initialize(deployer, {"from": deployer})
metaVault = deployer.deploy(MetaVault, curveEURTToken, bowswap)
eurs = Contract.from_explorer(curveEURSToken)
eurt = Contract.from_explorer(curveEURTToken)

curveEURSVaultContract = Contract.from_abi('curveEURSVault', curveEURSVault, VAULT_ABI)
curveEURTVaultContract = Contract.from_abi('curveEURTVault', curveEURTVault, VAULT_ABI)
curveibEURVaultContract = Contract.from_abi('curveibEURVault', curveibEURVault, VAULT_ABI)
curveEURNVaultContract = Contract.from_abi('curveEURNVault', curveEURNVault, VAULT_ABI)
curve3EURVaultContract = Contract.from_abi('curve3EURVault', curve3EURVault, VAULT_ABI)

def simulate_harvest(token, whale, vault):
	print('SIMULATING HARVEST WITH 100_000_000 USDC EARNED')
	token.transfer(vault, 100000000e18, {'from': whale})

def simulate_loss(vault):
	print('SIMULATING LOSS WITH 10_000 EUR LOSSED')
	Contract.from_explorer(curveibEURToken).transfer("0xe2F72C9A4CC773cFC5B3eAA148a15402B9a87441", 10000e18, {'from': curveibEURVault}) #Random address

def print_vault_PPS():
	curveEURSVaultShare = float('{0:.2f}'.format(curveEURSVaultContract.pricePerShare().to('ether')))
	curveEURTVaultShare = float('{0:.2f}'.format(curveEURTVaultContract.pricePerShare().to('ether')))
	curveibEURVaultShare = float('{0:.2f}'.format(curveibEURVaultContract.pricePerShare().to('ether')))
	curveEURNVaultShare = float('{0:.2f}'.format(curveEURNVaultContract.pricePerShare().to('ether')))
	curve3EURVaultShare = float('{0:.2f}'.format(curve3EURVaultContract.pricePerShare().to('ether')))
	print('\n-- PRICES PER SHARE ------------------------------')
	print('yv-curveEURS Share: ' + convert.to_string(curveEURSVaultShare))
	print('yv-curveEURT Share: ' + convert.to_string(curveEURTVaultShare))
	print('yv-curveibEUR Share: ' + convert.to_string(curveibEURVaultShare))
	print('yv-curveEURN Share: ' + convert.to_string(curveEURNVaultShare))
	print('yv-curve3EUR Share: ' + convert.to_string(curve3EURVaultShare))
	print('--------------------------------------------------')


def print_situation():
	vaultPPS = float('{0:.2f}'.format(metaVault.underlyingPricePerShare().to('ether')))
	depositorShare = float('{0:.2f}'.format(metaVault.getShares(depositor).to('ether')))
	anotherDepositorShare = float('{0:.2f}'.format(metaVault.getShares(another_depositor).to('ether')))
	thirdDepositorShare = float('{0:.2f}'.format(metaVault.getShares(third_depositor).to('ether')))
	print('\n-- METAVAULT DATA --------------------------------')
	print('TotalShare: ' + convert.to_string(metaVault.metaVaultTotalShare().to('ether')))
	print('Power: ' + convert.to_string(metaVault.power().to('ether')))
	print('Underlying PPS: ' + convert.to_string(metaVault.underlyingPricePerShare().to('ether')))
	print('Depositor Share: ' + convert.to_string(metaVault.getShares(depositor).to('ether')) + ' (' + str(round(vaultPPS * depositorShare)) + '$)')
	print('Another Depositor Share: ' + convert.to_string(metaVault.getShares(another_depositor).to('ether')) + ' (' + str(round(vaultPPS * anotherDepositorShare)) + '$)')
	print('Third Depositor Share: ' + convert.to_string(metaVault.getShares(third_depositor).to('ether')) + ' (' + str(round(vaultPPS * thirdDepositorShare)) + '$)')
	print('--------------------------------------------------')

def init_metavault():
	assert metaVault.metaVaultTotalShare() == 0
	assert metaVault.getShares(depositor) == 0

	# Take some eurs from the whales to work with
	eurt.transfer(depositor, 100000e18, {'from': curveEURTTokenWhale})
	assert eurt.balanceOf(depositor) >= 100000e18
	eurt.transfer(another_depositor, 50000e18, {'from': curveEURTTokenWhale})
	assert eurt.balanceOf(another_depositor) >= 50000e18

	# Deposit some eurt from depositor
	eurt.approve(metaVault.address, 100000e18, {'from': depositor})
	assert eurt.allowance(depositor, metaVault.address) == 100000e18
	metaVault.deposit(100000e18, depositor, {'from': depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 100000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 100000e18, abs=1e18)

	# Deposit some eurt from another_depositor
	eurt.approve(metaVault.address, 50000e18, {'from': another_depositor})
	assert eurt.allowance(another_depositor, metaVault.address) == 50000e18
	metaVault.deposit(50000e18, another_depositor, {'from': another_depositor})
	assert pytest.approx(metaVault.getShares(depositor), 100000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 50000e18, abs=1e18)

	# # Withdraw some eurt from depositor
	# metaVault.withdraw(50000e18, depositor, {'from': depositor})
	# assert pytest.approx(metaVault.metaVaultTotalShare(), 100000e18, abs=1e18)
	# assert pytest.approx(metaVault.getShares(depositor), 50000e18, abs=1e18)
	# assert pytest.approx(metaVault.getShares(another_depositor), 50000e18, abs=1e18)
	# assert pytest.approx(eurt.balanceOf(depositor), 50000e18, abs=1e18)

	# # Withdraw some eurt from another_depositor
	# metaVault.withdraw(50000e18, another_depositor, {'from': another_depositor})
	# assert pytest.approx(metaVault.metaVaultTotalShare(), 50000e18, abs=1e18)
	# assert pytest.approx(metaVault.getShares(depositor), 50000e18, abs=1e18)
	# assert pytest.approx(metaVault.getShares(another_depositor), 0, abs=1e18)
	# assert pytest.approx(eurt.balanceOf(another_depositor), 500, abs=1e18)

	# # Re-deposit some eurt from depositor and another_depositor
	# eurt.approve(metaVault.address, 50000e18, {'from': depositor})
	# assert eurt.allowance(depositor, metaVault.address) == 50000e18
	# metaVault.deposit(50000e18, depositor, {'from': depositor})
	# assert pytest.approx(metaVault.metaVaultTotalShare(), 100000e18, abs=1e18)
	# assert pytest.approx(metaVault.getShares(depositor), 100000e18, abs=1e18)
	# assert pytest.approx(metaVault.getShares(another_depositor), 0, abs=1e18)
	# assert pytest.approx(eurt.balanceOf(depositor), 0, abs=1e18)
	# eurt.approve(metaVault.address, 50000e18, {'from': another_depositor})
	# assert eurt.allowance(another_depositor, metaVault.address) == 50000e18
	# metaVault.deposit(50000e18, another_depositor, {'from': another_depositor})
	# assert pytest.approx(metaVault.metaVaultTotalShare(), 1500e18, abs=1e18)
	# assert pytest.approx(metaVault.getShares(depositor), 100000e18, abs=1e18)
	# assert pytest.approx(metaVault.getShares(another_depositor), 50000e18, abs=1e18)
	# assert pytest.approx(eurt.balanceOf(another_depositor), 0, abs=1e18)

def migrate(to, path):
	estimateOut = metaVault.estimateMigration(to, path)
	assert pytest.approx(estimateOut, 100000e18, abs=10e18)
	metaVault.swap(to, estimateOut * 0.1, path, {'from': deployer})
	assert pytest.approx(metaVault.power(), 1e18, abs=1e17)
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e6, abs=1e6)
	assert pytest.approx(metaVault.getShares(depositor), 100000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 50000e18, abs=1e18)
	print_situation()
	print_vault_PPS()

# def main():
# 	init_metavault()

# 	print_situation()
# 	print_vault_PPS()

# 	print('--> Migration from EURT to ibEUR <--')
# 	migrate(to = curveibEURToken, path = PATH_EURT_TO_IBEUR)
	# print('--> Migration from ibEUR to EURT <--')
	# migrate(to = curveEURTToken, path = PATH_IBEUR_TO_EURT)
	
	# migrate(to = curveEURNToken, path = PATH_IBEUR_TO_EURN)
	# migrate(to = curve3EURToken, path = PATH_EURN_TO_3EUR)
	# migrate(to = curveEURSToken, path = PATH_3EUR_TO_EURS)
	# migrate(to = curveEURNToken, path = PATH_EURS_TO_EURN)
	# migrate(to = curveEURTToken, path = PATH_EURN_TO_EURT)



































def testestest():
	eurt.transfer(depositor, 10000e18, {'from': curveEURTTokenWhale})
	eurt.approve(metaVault.address, 10000e18, {'from': depositor})
	metaVault.deposit(10000e18, depositor, {'from': depositor})
	print_situation()
	print_vault_PPS()

	eurs.transfer(curveEURSVaultContract, 10000000e18, {'from': curveEURSTokenWhale})
	print_vault_PPS()

	to = curveEURSToken
	path = PATH_EURT_TO_EURS
	estimateOut = metaVault.estimateMigration(to, path)
	metaVault.swap(to, estimateOut * 0.1, path, {'from': deployer})
	print_situation()
	print_vault_PPS()

	# A new player join the game!
	eurs.transfer(another_depositor, 40000e18, {'from': curveEURSTokenWhale})
	eurs.approve(metaVault.address, 40000e18, {'from': another_depositor})
	metaVault.deposit(40000e18, another_depositor, {'from': another_depositor})
	print_situation()
	print_vault_PPS()


	# The old player upgrade his game
	eurs.transfer(depositor, 10000e18, {'from': curveEURSTokenWhale})
	eurs.approve(metaVault.address, 10000e18, {'from': depositor})
	metaVault.deposit(10000e18, depositor, {'from': depositor})
	print_situation()
	print_vault_PPS()


	to = curveEURTToken
	path = PATH_EURS_TO_EURT
	estimateOut = metaVault.estimateMigration(to, path)
	metaVault.swap(to, estimateOut * 0.1, path, {'from': deployer})
	print_situation()
	print_vault_PPS()

	# The third depositor is adding some tokens too
	eurt.transfer(third_depositor, 10000e18, {'from': curveEURTTokenWhale})
	eurt.approve(metaVault.address, 10000e18, {'from': third_depositor})
	metaVault.deposit(10000e18, third_depositor, {'from': third_depositor})
	print_situation()
	print_vault_PPS()


def main():
	testestest()

