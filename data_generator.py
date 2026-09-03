# data_generator.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_finops_data(days=90):
    np.random.seed(42)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    providers = ['AWS', 'Azure']
    services = {
        'AWS': ['EC2', 'RDS', 'S3', 'EKS', 'Lambda'],
        'Azure': ['Virtual Machines', 'SQL Database', 'Blob Storage', 'AKS', 'Functions']
    }
    departments = ['Core Banking', 'Risk & Analytics', 'Payments API', 'DevOps & Infra']
    environments = ['Production', 'Staging', 'Development']
    
    records = []
    
    for date in dates:
        for provider in providers:
            for service in services[provider]:
                for dept in departments:
                    for env in environments:
                        # Coste base
                        base_cost = np.random.uniform(10, 150)
                        
                        # Factor de entorno
                        if env == 'Production':
                            base_cost *= 2.5
                        elif env == 'Development':
                            base_cost *= 0.6
                        
                        # Simulación de anomalía en un servicio
                        if provider == 'AWS' and service == 'EC2' and env == 'Development' and date > (end_date - timedelta(days=7)):
                            base_cost *= 3.8  # Anomalía: Instancias dev olvidadas encendidas
                            
                        records.append({
                            'Date': date,
                            'Provider': provider,
                            'Service': service,
                            'Department': dept,
                            'Environment': env,
                            'Cost_USD': round(base_cost, 2)
                        })
                        
    return pd.DataFrame(records)

if __name__ == '__main__':
    df = generate_finops_data()
    print(f"Datos generados exitosamente: {len(df)} filas.")
