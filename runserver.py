# A useful debugging script. Don't run this in production.

from balance.flask_app import app
app.run(debug=True)
