from EssembleRestClient import EssembleRestClient

def run(serviceName, featureService, operation):
    client = EssembleRestClient()
    params={'f': 'pjson'}
    variants = client.hit_server("Hockey_ADS_FS", True, "query", params)
    if variants:
        for v in variants:
            print('{seq_region_name}:{start}-{end}:{strand} ==> {id} ({consequence_type})'.format(**v));

if __name__ == '__main__':

    serviceName, featureService, operation = 'Hockey_ADS_FS', True, 'query'
    run(serviceName, featureService, operation) 