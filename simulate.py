import json
import logging
import random
from collections import Counter
from operator import itemgetter

from model import load_races

logger = logging.getLogger(__name__)


class NoBetsError(Exception):
    pass


def simulate(debug):
    """model results for best betting pattern"""
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.info('model results!')
    balance = 1000

    races = load_races()
    logger.info('Loaded {} races...'.format(len(races)))

    for strategy in [bet_positive_odds]:  # random_drop]:  # dutching_fav]:  # dutching]:  #]:  # ]:  #dutching_reverse
        book = []
        for race in races:
            # if race.race_type == 'G':
            #     continue

            bet_chunk = balance * 0.05
            runners = race.get_runners()
            # print(json.dumps(runners, indent=4, default=str, sort_keys=True))
            # return

            # drop scratched
            runners = [r for r in runners if r['win_odds']]
            if not runners:
                continue

            # default 0 bets
            for runner in runners:
                runner['bet'] = 0

            runners, num_bets = strategy(runners, bet_chunk)
            if num_bets:
                bet_results(book, runners, race.num_runners, bet_chunk, num_bets, race.race_type)
            # break

        logger.info('{}'.format(strategy.__name__))

        # races
        logger.info('Races: {}'.format(len(book)))

        # nums
        cw = Counter('{}/{}'.format(o['num_bets'], o['num_runners']) for o in book if o['success'])
        cl = Counter('{}/{}'.format(o['num_bets'], o['num_runners']) for o in book if not o['success'])
        logger.info('Num bets won = {}'.format(cw.most_common(5)))
        logger.info('Num bets los = {}'.format(cl.most_common(5)))

        # success
        success_ratio = sum([o['success'] for o in book]) / len(book)
        logger.info('Success = {:.0f}%'.format(success_ratio * 100))

        # profit
        profits = sum([o['profit'] for o in book])
        logger.info('Profit/race = {:.1f}'.format(profits / len(book)))
        total_inv = bet_chunk * len(book)
        roi = profits / total_inv
        logger.info('ROI = {:.1f}%'.format(roi * 100))

        # race types
        race_types = Counter('{}{}'.format(o['race_type'], int(o['success'])) for o in book)
        logger.info('Race types = {}'.format(race_types.most_common()))
        race_types_profits = {'Rp': 0, 'Gp': 0, 'Hp': 0, 'Ri': 0, 'Gi': 0, 'Hi': 0}
        for outcome in book:
            race_types_profits['{}i'.format(outcome['race_type'])] += bet_chunk
            race_types_profits['{}p'.format(outcome['race_type'])] += outcome['profit']
        for p, i in [('Rp', 'Ri'), ('Gp', 'Gi'), ('Hp', 'Hi')]:
            roi = race_types_profits[p] / race_types_profits[i]
            logger.info('ROI {}: {:.1f}%'.format(p, roi * 100))

        # ranks
        r = Counter(o['ranked'] for o in book)
        logger.info('ranked = {}'.format(r.most_common()))


def bet_results(book, runners, num_runners, bet_chunk, num_bets, race_type):
    win_diff = 0
    max_diff = 0
    outcome = {
        'success': 0,
        'profit': -bet_chunk,
        'num_bets': num_bets,
        'num_runners': num_runners,
    }
    for i, runner in enumerate(runners):
        diff = abs(runner['win_scaled'] - runner['probability'])
        max_diff = max(max_diff, diff)
        if int(runner['finishingPosition']) == 1:
            win_diff = diff
            if runner['bet'] > 0:
                # odds = runner['parimutuel']['returnWin'] if runner['parimutuel']['returnWin'] else runner['win_odds']
                odds = runner['win_odds']
                profit = runner['bet'] * odds - bet_chunk
                outcome = {
                    'success': 1,
                    'profit': profit,
                    'num_bets': num_bets,
                    'num_runners': num_runners,
                }
            break

    outcome['max_diff'] = max_diff
    outcome['win_diff'] = win_diff
    outcome['bet_chunk'] = bet_chunk
    outcome['race_type'] = race_type
    outcome['runners'] = runners
    book.append(outcome)


def bet_positive_dutch(runners, bet_chunk, bet_type, x):
    """dutch betting on probability"""
    pred = '{}_pred'.format(bet_type)
    prob = '{}_prob'.format(bet_type)
    bet = '{}_bet'.format(bet_type)

    # sort runners from favourite to underdog
    runners.sort(key=lambda r: r[pred], reverse=True)

    # start betting on all and cut off worse runner till positive outcome
    for num_bets in range(len(runners), 0, -1):

        # reset bets
        for runner in runners:
            runner[bet] = 0

        # recreate smaller pool
        pool = runners[:num_bets]
        # print('pool is {} from {} bets'.format(len(pool), num_bets))

        # all prediction values
        total_preds = sum([r[pred] for r in pool])

        # dutch for all in pool
        profits = []
        prob2scales = []
        for runner in pool:
            # scale bet according to prediction
            runner[bet] = bet_chunk * runner[pred] / total_preds

            # need to check all as we scale to probs and not odds
            profits.append(runner[bet] * runner['win_odds'] - bet_chunk)
            prob2scales.append(runner[prob] / runner['win_scaled'])

        ###################################################################################
        # MIN PROFIT
        ###################################################################################
        min_profit_flag = False
        min_profit = min(profits)
        if min_profit > bet_chunk * x[0]:
            min_profit_flag = True

        ###################################################################################
        # MIN PROB 2 SCALE
        ###################################################################################
        min_probs2scale_flag = False
        min_probs2scale = min(prob2scales)
        if min_probs2scale >= x[1]:
            min_probs2scale_flag = True

        if min_profit_flag and min_probs2scale_flag:
            # print('breaking: {} {} {} {}'.format(min_profit_flag, avg_profit_flag, num_bets_flag, min_probs2scale_flag))
            break

    else:
        #         print('no profit determined')
        raise NoBetsError()

    # put bets from pool into runners
    for p in pool:
        for r in runners:
            if r['runnerNumber'] == p['runnerNumber']:
                r[bet] = p[bet]
                break

    return runners, num_bets