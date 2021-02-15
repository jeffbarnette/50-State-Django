# Generated by Django 3.1.6 on 2021-02-13 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    def insertStateAndCapitalData(apps, schema_editor):
        """Populate 50 U.S. states and capitals"""
        # Source data
        states_and_capitals = [
            {'state': 'Alabama', 'abbr': 'AL', 'capital': 'Montgomery'},
            {'state': 'Alaska', 'abbr': 'AK', 'capital': 'Juneau'},
            {'state': 'Arizona', 'abbr': 'AZ', 'capital': 'Phoenix'},
            {'state': 'Arkansas', 'abbr': 'AR', 'capital': 'Little Rock'},
            {'state': 'California', 'abbr': 'CA', 'capital': 'Sacramento'},
            {'state': 'Colorado', 'abbr': 'CO', 'capital': 'Denver'},
            {'state': 'Connecticut', 'abbr': 'CT', 'capital': 'Hartford'},
            {'state': 'Delaware', 'abbr': 'DE', 'capital': 'Dover'},
            {'state': 'Florida', 'abbr': 'FL', 'capital': 'Tallahassee'},
            {'state': 'Georgia', 'abbr': 'GA', 'capital': 'Atlanta'},
            {'state': 'Hawaii', 'abbr': 'HI', 'capital': 'Honolulu'},
            {'state': 'Idaho', 'abbr': 'ID', 'capital': 'Boise'},
            {'state': 'Illinois', 'abbr': 'IL', 'capital': 'Springfield'},
            {'state': 'Indiana', 'abbr': 'IN', 'capital': 'Indianapolis'},
            {'state': 'Iowa', 'abbr': 'IA', 'capital': 'Des Moines'},
            {'state': 'Kansas', 'abbr': 'KS', 'capital': 'Topeka'},
            {'state': 'Kentucky', 'abbr': 'KY', 'capital': 'Frankfort'},
            {'state': 'Louisiana', 'abbr': 'LA', 'capital': 'Baton Rouge'},
            {'state': 'Maine', 'abbr': 'ME', 'capital': 'Augusta'},
            {'state': 'Maryland', 'abbr': 'MD', 'capital': 'Annapolis'},
            {'state': 'Massachusetts', 'abbr': 'MA', 'capital': 'Boston'},
            {'state': 'Michigan', 'abbr': 'MI', 'capital': 'Lansing'},
            {'state': 'Minnesota', 'abbr': 'MN', 'capital': 'Saint Paul'},
            {'state': 'Mississippi', 'abbr': 'MS', 'capital': 'Jackson'},
            {'state': 'Missouri', 'abbr': 'MO', 'capital': 'Jefferson City'},
            {'state': 'Montana', 'abbr': 'MT', 'capital': 'Helena'},
            {'state': 'Nebraska', 'abbr': 'NE', 'capital': 'Lincoln'},
            {'state': 'Nevada', 'abbr': 'NV', 'capital': 'Carson City'},
            {'state': 'New Hampshire', 'abbr': 'NH', 'capital': 'Concord'},
            {'state': 'New Jersey', 'abbr': 'NJ', 'capital': 'Trenton'},
            {'state': 'New Mexico', 'abbr': 'NM', 'capital': 'Santa Fe'},
            {'state': 'New York', 'abbr': 'NY', 'capital': 'Albany'},
            {'state': 'North Carolina', 'abbr': 'NC', 'capital': 'Raleigh'},
            {'state': 'North Dakota', 'abbr': 'ND', 'capital': 'Bismarck'},
            {'state': 'Ohio', 'abbr': 'OH', 'capital': 'Columbus'},
            {'state': 'Oklahoma', 'abbr': 'OK', 'capital': 'Oklahoma City'},
            {'state': 'Oregon', 'abbr': 'OR', 'capital': 'Salem'},
            {'state': 'Pennsylvania', 'abbr': 'PA', 'capital': 'Harrisburg'},
            {'state': 'Rhode Island', 'abbr': 'RI', 'capital': 'Providence'},
            {'state': 'South Carolina', 'abbr': 'SC', 'capital': 'Columbia'},
            {'state': 'South Dakota', 'abbr': 'SD', 'capital': 'Pierre'},
            {'state': 'Tennessee', 'abbr': 'TN', 'capital': 'Nashville'},
            {'state': 'Texas', 'abbr': 'TX', 'capital': 'Austin'},
            {'state': 'Utah', 'abbr': 'UT', 'capital': 'Salt Lake City'},
            {'state': 'Vermont', 'abbr': 'VT', 'capital': 'Montpelier'},
            {'state': 'Virginia', 'abbr': 'VA', 'capital': 'Richmond'},
            {'state': 'Washington', 'abbr': 'WA', 'capital': 'Olympia'},
            {'state': 'West Virginia', 'abbr': 'WV', 'capital': 'Charleston'},
            {'state': 'Wisconsin', 'abbr': 'WI', 'capital': 'Madison'},
            {'state': 'Wyoming', 'abbr': 'WY', 'capital': 'Cheyenne'}
        ]

        # Get the models
        State = apps.get_model('location', 'State')
        Capital = apps.get_model('location', 'Capital')

        # Populate Database
        for state_entry in states_and_capitals:
            # Add State Capital
            capital = Capital(name=state_entry['capital'])
            capital.save()
            # Add State
            state = State(
                name=state_entry['state'],
                abbr=state_entry['abbr'],
                capital=Capital(id=capital.id)
            )
            state.save()

    operations = [
        migrations.RunPython(insertStateAndCapitalData),
    ]
