import requests
import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import core.models


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """This command gets Pokemons information from pokeapi.co
    and insert the data to the database through the ORM
    """
    help = 'Populate database with pokemon information from pokeapi.co'

    def _check_response_status(self, request):
        if request.status_code != 200:
            logger.error(f'Got a {request.status_code} status code while requesting from pokeapi.co')
            raise CommandError(
                'Something went wrong while requesting pokemons info\n\n'
                f'Response status code = {request.status_code}\n'
                f'Response body:\n<<\n{request.text}\n>>'
            )


    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type = int,
            help = 'limits the number of pokemons that are added'
                ' to the database. Default is 20, the maximum is 100 pokemon.'
        )

    def handle(self, *args, **options):
        limit = options.get('limit')
        if limit is None:
            limit = 20

        if 100 < limit or limit <= 0:
            raise CommandError("The value of the argument 'limit' must be from 1 to 100")

        if core.models.Pokemon.objects.all().exists():
            raise CommandError('The database has already been populated.')

        
        logger.info(f'Requesting {limit} pokemons data to remote api')

        # If any errors occur while inserting data, roll back the entire transaction
        with transaction.atomic():

            poke_response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit={limit}')

            self._check_response_status(poke_response)

            pokemons_list = poke_response.json()['results']
            
            for pokemon_reference in pokemons_list:
                pokemon_response = requests.get(pokemon_reference['url'])

                self._check_response_status(pokemon_response)
                
                poke_info = pokemon_response.json()

                pokemon_obj = core.models.Pokemon.objects.create(
                    name=poke_info['name'],
                    height=poke_info['height'],
                    weight=poke_info['weight']
                )

                logger.info(f'---- {pokemon_obj.name} has been inserted.')

                for ability in poke_info['abilities']:
                    pokemon_obj.abilities.create(name=ability['ability']['name'])
            



            

        
        