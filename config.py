# **** Server configuration ****

# Bind address
bind_address = "0.0.0.0"

# Bind port
bind_port = 1337

# Server banner
server_banner = "ESMTP Postfix (Debian/GNU)"

# Served domain. This will be used when authentication is enabled.
served_domain = "mail.example.com"

# Credentials file. Set to None if you don't want any.
# The format of the file should be:
#
# user1:pass1
# user2:pass2
# ...
credentials_file = None
