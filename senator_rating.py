import csv
import json
import re
import utils
import datetime
from utils import load_data, save_data


def main():
    # load in members, orient by bioguide ID
    # yaml file from - https://github.com/unitedstates/congress-legislators
    print("Loading current legislators...")
    current = load_data("legislators-current.yaml")

    # type, start, end, tenure
    tenures = []
    current_rep = {}
    current_senate = {}
    last_term = {}
    ###
    #   each member has rep start and end term, calculated tenure
    #   each member has sen start and end term, calculated tenure
    #   each member current(last term) type, start and end term
    #   'id':
    #       rep:
    #          first:
    #           last:
    #           tenure:
    #       senate:
    #          first:
    #           last:
    #           tenure:
    #       current:
    #           type:
    #           start:
    #           end:
    ###
    for m in current:
        current_id = m['id']['bioguide']
        current_rep = {}
        current_senate = {}
        last_term = {}
        for t in m['terms']:
            # capture type, start/end date
            # compare next type
            # if match add compute tenure by updating end date
            # else store current tenure and start tenure capturing type, start/end date
            # compute total tenure across types
            start_date_obj = datetime.datetime.strptime(t['start'], '%Y-%m-%d')
            end_date_obj = datetime.datetime.strptime(t['end'], '%Y-%m-%d')
            term_duration = (end_date_obj.year - start_date_obj.year)
            last_term = t
            if t['type'] == 'rep':
                if current_rep:
                    c_end_obj = current_rep['last']
                    c_start_date = datetime.datetime.strptime(
                        c_end_obj['start'], '%Y-%m-%d')
                    c_end_date = datetime.datetime.strptime(
                        c_end_obj['end'], '%Y-%m-%d')
                    # compare current end date to new start date (Consecutive)
                    # if end date year == start date year
                    #   then tenure = tenure + (new end date - current end date)
                    #   update current end date
                    # if c_end_date.year == start_date_obj.year:
                    current_rep['tenure'] = current_rep['tenure'] + \
                        term_duration
                    current_rep['last'] = t
                    # else (*not Consecutive*)
                    #   then tenure = tenure + (new end date - new start date)
                    #   update current start end date

                else:
                    # update current rep type, start, end, tenure
                    current_rep = {
                        'first': t,
                        'last': t,
                        'tenure': end_date_obj.year - start_date_obj.year
                    }
            else:
                if current_senate:
                    current_senate['tenure'] = current_senate['tenure'] + \
                        term_duration
                    current_senate['last'] = t
                else:
                    # update current rep type, start, end, tenure
                    current_senate = {
                        'first': t,
                        'last': t,
                        'tenure': end_date_obj.year - start_date_obj.year
                    }
        tenures.append({
            'id': current_id,
            'rep': current_rep,
            'senate': current_senate,
            'current': last_term})
    print(tenures)


if __name__ == '__main__':
    main()
