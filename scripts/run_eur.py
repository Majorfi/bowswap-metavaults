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
bowswap = deployer.deploy(VaultSwapper)
bowswap.initialize(deployer, {"from": deployer})
metaVault = deployer.deploy(MetaVault, curveEURTToken, bowswap)
eurs = Contract.from_explorer(curveEURSToken)
eurt = Contract.from_explorer(curveEURTToken)

curveEURSVaultContract = Contract.from_explorer(curveEURSVault)
curveEURTVaultContract = Contract.from_explorer(curveEURTVault)
curveibEURVaultContract = Contract.from_explorer(curveibEURVault)
curveEURNVaultContract = Contract.from_explorer(curveEURNVault)
curve3EURVaultContract = Contract.from_explorer(curve3EURVault)

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
	print('\n-- METAVAULT DATA --------------------------------')
	print('TotalShare: ' + convert.to_string(metaVault.metaVaultTotalShare().to('ether')))
	print('Underlying PPS: ' + convert.to_string(metaVault.underlyingPricePerShare().to('ether')))
	print('Depositor Share: ' + convert.to_string(metaVault.getShares(depositor).to('ether')) + ' (' + str(round(vaultPPS * depositorShare)) + '$)')
	print('Another Depositor Share: ' + convert.to_string(metaVault.getShares(another_depositor).to('ether')) + ' (' + str(round(vaultPPS * anotherDepositorShare)) + '$)')
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
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1500e18, abs=1e18)
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

def main():
	init_metavault()

	print_situation()
	print_vault_PPS()

	print('--> Migration from EURT to ibEUR <--')
	migrate(to = curveibEURToken, path = PATH_EURT_TO_IBEUR)
	print('--> Migration from ibEUR to EURT <--')
	migrate(to = curveEURTToken, path = PATH_IBEUR_TO_EURT)
	
	# migrate(to = curveEURNToken, path = PATH_IBEUR_TO_EURN)
	# migrate(to = curve3EURToken, path = PATH_EURN_TO_3EUR)
	# migrate(to = curveEURSToken, path = PATH_3EUR_TO_EURS)
	# migrate(to = curveEURNToken, path = PATH_EURS_TO_EURN)
	# migrate(to = curveEURTToken, path = PATH_EURN_TO_EURT)

