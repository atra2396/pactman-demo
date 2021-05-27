from pactman.verifier.verify import ProviderStateMissing
import requests

def provider_state(name, **params):
    print(params)
    if name == "item with id 0 exists":
        state = requests.post("http://localhost:8000/_pact/setup_provider_state", json={ "state": "item with id 0 exists" })
        state.raise_for_status()
    elif name == "item with if 0 exists with 0 stock":
        state = requests.post("http://localhost:8000/_pact/setup_provider_state", json={ "state": "item with if 0 exists with 0 stock" })
        state.raise_for_status()
    else:
        raise ProviderStateMissing(name)

def test_pacts(pact_verifier):
    pact_verifier.verify(provider_setup=provider_state, provider_url="http://localhost:8000")