# Maple API script

import maple.api as maple

maple = maple.Maple()

maple.image.build()
maple.container.execute("pwd")
maple.image.clean()
