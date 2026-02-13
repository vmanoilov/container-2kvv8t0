from typing import List

class Planner:
    @staticmethod
    def get_stages(profile: str) -> List[str]:
        if profile == 'quick':
            return ['recon']
        elif profile == 'standard':
            return ['recon', 'web']
        elif profile == 'deep':
            return ['recon', 'web', 'vuln']
        else:
            return ['recon', 'web', 'vuln']  # default to deep

    @staticmethod
    def get_next_stage(current_stage: str, profile: str) -> str:
        stages = Planner.get_stages(profile)
        try:
            idx = stages.index(current_stage)
            if idx + 1 < len(stages):
                return stages[idx + 1]
            else:
                return 'complete'
        except ValueError:
            return 'complete'