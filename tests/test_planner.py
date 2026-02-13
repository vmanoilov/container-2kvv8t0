from app.coordinator.planner import Planner

def test_get_stages():
    assert Planner.get_stages('quick') == ['recon']
    assert Planner.get_stages('standard') == ['recon', 'web']
    assert Planner.get_stages('deep') == ['recon', 'web', 'vuln']
    assert Planner.get_stages('unknown') == ['recon', 'web', 'vuln']

def test_get_next_stage():
    assert Planner.get_next_stage('recon', 'standard') == 'web'
    assert Planner.get_next_stage('web', 'standard') == 'complete'
    assert Planner.get_next_stage('recon', 'quick') == 'complete'
    assert Planner.get_next_stage('unknown', 'standard') == 'complete'