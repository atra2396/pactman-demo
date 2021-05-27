import requests
from pactman.verifier.verify import ProviderStateMissing

def provider_state(name, **params):
    if name == "item with id 0 has price 10":
        state = requests.post("http://localhost:8000/_pact/setup_provider_state", json={ "state": "item with id 0 has price 10" })
        state.raise_for_status()
    else:
        raise ProviderStateMissing(name)

def test_pacts(pact_verifier):
    pact_verifier.verify(provider_setup=provider_state, provider_url="http://localhost:8000")