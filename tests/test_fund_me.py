from _pytest.config import exceptions
from scripts.helpful_scripts import *
from scripts.deploy import deploy_fund_me
from brownie import *
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fm = deploy_fund_me()
    entrance_fee = fm.getEntranceFee() + 100
    tx = fm.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fm.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fm.withdraw({"from": account})
    tx2.wait
    assert fm.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    fm = deploy_fund_me()
    bad_actor = accounts.add()
    fm.withdraw({"from": politic})
    with pytest.raises(exceptions.VirtualMachineError):
        fm.withdraw({"from": politic})
