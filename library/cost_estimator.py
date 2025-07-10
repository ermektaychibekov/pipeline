#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import json

class CostEstimator:
    PROVIDER_RATES = {
        'aws': {'development': 0.02, 'staging': 0.05, 'production': 0.12},
        'gcp': {'development': 0.018, 'staging': 0.048, 'production': 0.11},
        'azure': {'development': 0.022, 'staging': 0.055, 'production': 0.13}
    }
    
    def calculate(self, providers, environment, duration):
        total = 0.0
        for provider in providers:
            rate = self.PROVIDER_RATES.get(provider, {}).get(environment, 0)
            total += rate * duration
        return round(total, 4)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            providers=dict(type='list', required=True),
            environment=dict(type='str', required=True),
            duration_minutes=dict(type='int', required=True)
        ),
        supports_check_mode=True
    )
    
    estimator = CostEstimator()
    cost = estimator.calculate(
        module.params['providers'],
        module.params['environment'],
        module.params['duration_minutes'] / 60
    )
    
    result = {
        'estimated_cost': cost,
        'calculation_parameters': module.params
    }
    
    module.exit_json(changed=False, **result)

if __name__ == '__main__':
    main()
