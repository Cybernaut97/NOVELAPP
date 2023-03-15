class AddToFreezerForm(FlaskForm):
    flavor = QuerySelectField('Flavor', query_factory=lambda: Flavor.query.all(), get_label='name')
    submit = SubmitField('Add to Freezer')