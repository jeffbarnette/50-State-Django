from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from .models import State, Capital


class TestModels(TestCase):
    def test_states_are_prepopulated_in_db(self):
        """Test that states are pre-populated at db creation."""
        state_count = State.objects.count()
        self.assertGreaterEqual(state_count, 50)

    def test_capitals_are_prepopulated_in_db(self):
        """Test that capitals are pre-populated at db creation."""
        capital_count = Capital.objects.count()
        self.assertGreaterEqual(capital_count, 50)

    def test_state_name_string_representation(self):
        """Test that state has name string representation."""
        new_capital = Capital.objects.create(name='Test')
        new_state = State.objects.create(
            name='Test',
            abbr='TS',
            capital=Capital(id=new_capital.id)
        )
        test_state = State.objects.get(id=new_state.id)
        self.assertEqual(str(test_state), new_state.name)

    def test_capital_name_string_representation(self):
        """Test that Capital has name string representation."""
        new_capital = Capital.objects.create(name='Test')
        test_capital = Capital.objects.get(id=new_capital.id)
        self.assertEqual(str(test_capital), new_capital.name)

    def test_state_has_a_name_abbreviation_and_capital(self):
        """Test that State has a name, abbreviation and capital."""
        new_capital = Capital.objects.create(name='Test')
        new_state = State.objects.create(
            name='Test',
            abbr='TS',
            capital=Capital(id=new_capital.id)
        )
        self.assertEqual(new_state.name, 'Test')
        self.assertEqual(new_state.abbr, 'TS')
        self.assertEqual(new_state.capital.id, new_capital.id)

    def test_capital_has_a_name(self):
        """Test that Capital has a name."""
        new_capital = Capital.objects.create(name='Test')
        test_capital = Capital.objects.get(id=new_capital.id)
        self.assertEqual(test_capital.name, 'Test')

    def test_error_when_state_name_is_null(self):
        """Test that an error is returned when state name is null."""
        error_msg = None
        try:
            with transaction.atomic():
                new_capital = Capital.objects.create(name='Test')
                State.objects.create(
                    name=None,
                    abbr='TS',
                    capital=Capital(id=new_capital.id)
                )
        except IntegrityError as e:
            error_msg = str(e).split(':')

        self.assertIn('null value in column "name"', error_msg[0])

    def test_error_when_state_abbreviation_is_null(self):
        """Test that an error is returned when abbreviation is null."""
        error_msg = None
        try:
            with transaction.atomic():
                new_capital = Capital.objects.create(name='Test')
                State.objects.create(
                    name='Test',
                    abbr=None,
                    capital=Capital(id=new_capital.id)
                )
        except IntegrityError as e:
            error_msg = str(e).split(':')

        self.assertIn('null value in column "abbr"', error_msg[0])

    def test_error_when_capital_is_null(self):
        """Test that an error is returned when capital is null."""
        error_msg = None
        try:
            with transaction.atomic():
                State.objects.create(
                    name='Test',
                    abbr='TS',
                    capital=None
                )
        except IntegrityError as e:
            error_msg = str(e).split(':')

        self.assertIn('null value in column "capital_id"', error_msg[0])

    def test_error_when_capital_name_is_null(self):
        """Test that an error is returned when capital name is null."""
        error_msg = None
        try:
            with transaction.atomic():
                Capital.objects.create(name=None)
        except IntegrityError as e:
            error_msg = str(e).split(':')

        self.assertIn('null value in column "name"', error_msg[0])

    def test_state_name_auto_capitalized_on_save(self):
        """Test that the state name is automatically capitalized."""
        new_capital = Capital.objects.create(name='Test')
        new_state = State.objects.create(
            name='test',
            abbr='TS',
            capital=Capital(id=new_capital.id)
        )
        test_state = State.objects.get(id=new_state.id)
        self.assertEqual(test_state.name, 'Test')

    def test_state_abbreviation_auto_capitalized_on_save(self):
        """Test that the state abbreviation is automatically capitalized."""
        new_capital = Capital.objects.create(name='Test')
        new_state = State.objects.create(
            name='test',
            abbr='ts',
            capital=Capital(id=new_capital.id)
        )
        test_state = State.objects.get(id=new_state.id)
        self.assertEqual(test_state.abbr, 'TS')

    def test_capital_name_auto_capitalized_on_save(self):
        """Test that the capital name is automatically capitalized."""
        new_capital = Capital.objects.create(name='test')
        test_capital = Capital.objects.get(id=new_capital.id)
        self.assertEqual(test_capital.name, 'Test')

    def test_error_when_state_name_is_not_unique(self):
        """Test that error is returned when state name is not unqiue."""
        error_msg = None
        try:
            with transaction.atomic():
                new_capital = Capital.objects.create(name='Test')
                State.objects.create(
                    name='Alabama',
                    abbr='TS',
                    capital=Capital(id=new_capital.id)
                )
        except IntegrityError as e:
            error_msg = str(e).split(':')

        self.assertIn(
            'duplicate key value violates unique constraint', error_msg[0])

    def test_error_when_state_abbreviation_is_not_unique(self):
        """Test that error is returned when state abbr is not unqiue."""
        error_msg = None
        try:
            with transaction.atomic():
                new_capital = Capital.objects.create(name='Test')
                State.objects.create(
                    name='Test',
                    abbr='AL',
                    capital=Capital(id=new_capital.id)
                )
        except IntegrityError as e:
            error_msg = str(e).split(':')

        self.assertIn(
            'duplicate key value violates unique constraint', error_msg[0])

    def test_error_when_capital_name_is_not_unique(self):
        """Test that error is returned when capital name is not unique."""
        error_msg = None
        try:
            with transaction.atomic():
                new_capital = Capital.objects.create(name='Montgomery')
                State.objects.create(
                    name='Test',
                    abbr='TS',
                    capital=Capital(id=new_capital.id)
                )
        except IntegrityError as e:
            error_msg = str(e).split(':')

        self.assertIn(
            'duplicate key value violates unique constraint', error_msg[0])

    def test_only_alpha_characters_allowed_with_state_name_and_abbr(self):
        """
        Test that error is returned when non-alpha characters are
        entered for state name and abbreviation.
        """
        # State name
        new_capital = Capital.objects.create(name='Test')
        new_state = State.objects.create(
            name='123',
            abbr='TS',
            capital=Capital(id=new_capital.id)
        )
        try:
            new_state.full_clean()
        except ValidationError as e:
            self.assertTrue('name' in e.message_dict)
            self.assertEqual(
                e.message_dict['name'][0],
                'Only alpha characters are allowed.')

        # State abbreviation
        new_state = State.objects.create(
            name='Test2',
            abbr='12',
            capital=Capital(id=new_capital.id)
        )
        try:
            new_state.full_clean()
        except ValidationError as e:
            self.assertTrue('abbr' in e.message_dict)
            self.assertEqual(
                e.message_dict['abbr'][0],
                'Only alpha characters are allowed.')

    def test_only_alpha_characters_allowed_with_capital_name(self):
        """
        Test that error is returned when non-alpha characters are
        entered for capital name.
        """
        new_capital = Capital.objects.create(name='123')
        try:
            new_capital.full_clean()
        except ValidationError as e:
            self.assertTrue('name' in e.message_dict)
            self.assertEqual(
                e.message_dict['name'][0],
                'Only alpha characters are allowed.')


class TestView(TestCase):
    valid_states = [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
        'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
        'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
        'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
        'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
        'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
        'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
        'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
        'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
        'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
    ]

    valid_abbrs = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
        'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI',
        'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
        'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
        'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ]

    valid_capitals = [
        'Montgomery', 'Juneau', 'Phoenix', 'Little Rock', 'Sacramento',
        'Denver', 'Hartford', 'Dover', 'Tallahassee', 'Atlanta',
        'Honolulu', 'Boise', 'Springfield', 'Indianapolis', 'Des Moines',
        'Topeka', 'Frankfort', 'Baton Rouge', 'Augusta', 'Annapolis',
        'Boston', 'Lansing', 'Saint Paul', 'Jackson', 'Jefferson City',
        'Helena', 'Lincoln', 'Carson City', 'Concord', 'Trenton',
        'Santa Fe', 'Albany', 'Raleigh', 'Bismarck', 'Columbus',
        'Oklahoma City', 'Salem', 'Harrisburg', 'Providence', 'Columbia',
        'Pierre', 'Nashville', 'Austin', 'Salt Lake City', 'Montpelier',
        'Richmond', 'Olympia', 'Charleston', 'Madison', 'Cheyenne'

    ]

    def test_state_list_view_templates_used(self):
        """Test that state list view uses correct templates."""
        response = self.client.get(reverse('states'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'location/home.html')
        self.assertTemplateUsed(response, 'location/base.html')

    def test_state_list_view_returns_50_states(self):
        """Test that state list view returns 50 valid states."""
        response = self.client.get(reverse('states'))
        self.assertEqual(response.status_code, 200)

        # Verify there are 50 states
        state_count = len(response.context[0]['states'])
        self.assertEqual(state_count, 50)

        response_state_list = [
            str(state) for state in response.context[0]['states']
        ]
        # Check that each of the 50 states exists in response
        for state in self.valid_states:
            self.assertIn(state, response_state_list)

    def test_state_list_view_returns_50_state_capitals(self):
        """Test that state list view returns 50 valid state capitals."""
        response = self.client.get(reverse('states'))
        self.assertEqual(response.status_code, 200)

        # Verify there are 50 state capitals
        response_capital_list = [
            str(state.capital) for state in response.context[0]['states']
        ]
        capital_count = len(response_capital_list)
        self.assertEqual(capital_count, 50)

        # Check that each of the 50 state capitals exists in response
        for capital in self.valid_capitals:
            self.assertIn(capital, response_capital_list)

    def test_state_list_view_returns_correct_state_and_capital_pairing(self):
        """Test that StateListView returns correct capital for each state."""
        response = self.client.get(reverse('states'))
        self.assertEqual(response.status_code, 200)

        response_state_list = [
            str(state) for state in response.context[0]['states']
        ]

        response_abbrs_list = [
            str(state.abbr) for state in response.context[0]['states']
        ]

        response_capital_list = [
            str(state.capital) for state in response.context[0]['states']
        ]

        # Check that we have an equal number of states and capitals
        state_count = len(response.context[0]['states'])
        capital_count = len(response_capital_list)
        self.assertEqual(state_count, capital_count)

        # Check that each state has the correct abbreviation and capital
        valid_source_states = list(
            zip(
                self.valid_states,
                self.valid_abbrs,
                self.valid_capitals
            )
        )

        valid_response_states = list(
            zip(
                response_state_list,
                response_abbrs_list,
                response_capital_list
            )
        )

        self.assertEqual(valid_response_states, valid_source_states)

    def test_state_querystring_returns_state_details(self):
        """
        Test that the state querystring returns correct details
        for all 50 state names and abbreviations regardless of
        being lowercase, uppercase, or only having first letter
        capitalized.
        """
        states = State.objects.all()

        client = Client()

        for state in states:
            # Test only first letter of state name capitalized
            response = client.get('/', {'state': state.name})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                str(response.context[0]['states'][0]), state.name)
            self.assertEqual(
                str(response.context[0]['states'][0].abbr), state.abbr)
            self.assertEqual(
                str(response.context[0]['states'][0].capital),
                str(state.capital))

            # Test state name in all uppercase
            response = client.get('/', {'state': state.name.upper()})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                str(response.context[0]['states'][0]), state.name)
            self.assertEqual(
                str(response.context[0]['states'][0].abbr), state.abbr)
            self.assertEqual(
                str(response.context[0]['states'][0].capital),
                str(state.capital))

            # Test state name in all lowercase
            response = client.get('/', {'state': state.name.lower()})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                str(response.context[0]['states'][0]), state.name)
            self.assertEqual(
                str(response.context[0]['states'][0].abbr), state.abbr)
            self.assertEqual(
                str(response.context[0]['states'][0].capital),
                str(state.capital))

            # Test only first letter of state abbreviation name capitalized
            response = client.get('/', {'state': state.abbr.title()})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                str(response.context[0]['states'][0]), state.name)
            self.assertEqual(
                str(response.context[0]['states'][0].abbr), state.abbr)
            self.assertEqual(
                str(response.context[0]['states'][0].capital),
                str(state.capital))

            # Test state abbreviation in all uppercase
            response = client.get('/', {'state': state.abbr.upper()})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                str(response.context[0]['states'][0]), state.name)
            self.assertEqual(
                str(response.context[0]['states'][0].abbr), state.abbr)
            self.assertEqual(
                str(response.context[0]['states'][0].capital),
                str(state.capital))

            # Test state abbreviation in all lowercase
            response = client.get('/', {'state': state.abbr.lower()})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                str(response.context[0]['states'][0]), state.name)
            self.assertEqual(
                str(response.context[0]['states'][0].abbr), state.abbr)
            self.assertEqual(
                str(response.context[0]['states'][0].capital),
                str(state.capital))

    def test_capital_querystring_returns_state_details(self):
        """
        Test that the capital querystring returns correct details
        for all 50 state capital names regardless of being lowercase,
        uppercase, or only having the first letter capitalized.
        """
        states = State.objects.all()

        client = Client()

        for state in states:
            # Test only first letter capitalized
            response = client.get('/', {'capital': str(state.capital)})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                str(response.context[0]['states'][0]), state.name)
            self.assertEqual(
                str(response.context[0]['states'][0].abbr), state.abbr)
            self.assertEqual(
                str(response.context[0]['states'][0].capital),
                str(state.capital))

            # Test all uppercase
            response = client.get(
                '/', {'capital': str(state.capital).upper()})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                str(response.context[0]['states'][0]), state.name)
            self.assertEqual(
                str(response.context[0]['states'][0].abbr), state.abbr)
            self.assertEqual(
                str(response.context[0]['states'][0].capital),
                str(state.capital))

            # Test all lowercase
            response = client.get(
                '/', {'capital': str(state.capital).lower()})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                str(response.context[0]['states'][0]), state.name)
            self.assertEqual(
                str(response.context[0]['states'][0].abbr), state.abbr)
            self.assertEqual(
                str(response.context[0]['states'][0].capital),
                str(state.capital))

    def test_not_found_when_invalid_value_passed_into_querystrings(self):
        """Test that a message is returned when invalid value is passed."""
        client = Client()
        response = client.get('/', {'state': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context[0]['states'], {'message': 'State not found!'})

        response = client.get('/', {'capital': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context[0]['states'], {'message': 'Capital not found!'})
