from .models import *
from .pack_card import PackCard
from .card import Card

class Pack():
    #methods
    @staticmethod
    def get_packs(params):
        packs = select_items('packs', params)
        return packs

    @staticmethod
    def get_pack_by_id(id):
        pack = select_item_by_id('packs', id)
        return pack

    @staticmethod
    def create_pack(set_code, player_id, number):
        pack = insert_item('packs', {'set_code': set_code, 'player_id': player_id, 'number': number})
        booster_cards = SDKSet.generate_booster(set_code)
        print('Set SDK Call', file=sys.stderr)
        card_ids_used = []
        for booster_card in booster_cards:
            while booster_card.multiverse_id in card_ids_used:
                print('Inserting: %i into: %s' % (booster_card.multiverse_id, ','.join(str(e) for e in card_ids_used)), file=sys.stderr)
                replacement_cards = SDKCard.where(set=set_code).where(rarity=booster_card.rarity).all()
                booster_card = random.choice(replacement_cards)
                print('Card SDK Call', file=sys.stderr)
            existing_cards = select_items('cards', ["multiverse_id=%i" % booster_card.multiverse_id])
            if existing_cards:
                card = existing_cards[0]
            else:
                card = Card.create_card(booster_card.name, booster_card.image_url, booster_card.multiverse_id, booster_card.cmc, json.dumps(booster_card.colors), booster_card.set)
            card_ids_used.append(booster_card.multiverse_id)
            PackCard.create_pack_card(card['id'], pack['id'])
        return pack

    @staticmethod
    def update_packs(values, params):
        pack = update_item('packs', values, params)
        return pack

    @staticmethod
    def update_pack_by_id(id, values):
        return update_packs(values, ["id=%i", id])

    @staticmethod
    def delete_pack(id):
        pack = delete_item_with_id('packs', id)
        return true

    @staticmethod
    def get_available_cards(pack_id):
        pack = select_item_by_id('packs', pack_id)
        pack_cards = select_items('pack_cards', ["pack_id=%i" % pack_id, "deck_id IS NULL"])
        card_ids = [pack_card['id'] for pack_card in pack_cards]
        cards = select_items('cards', ["cards.id in (%s)" % ",".join(list(map(str, card_ids)))])
        card_images = {card['id']: card['image_url'] for card in cards}
        pack_cards = [dict({'image_url': card_images[pack_card['card_id']]}, **pack_card) for pack_card in pack_cards]
        return pack_cards

    @staticmethod
    def get_all_cards(pack_id):
        pack = select_item_by_id('packs', pack_id)
        pack_cards = select_items('pack_cards', ["pack_id=%i" % pack_id])
        return pack_cards
