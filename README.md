# Trader_binance
gateway trader


## How it's Work?
 - This is for send and recive data from binance with api
    Connect to binance with api key/secret,
    use python-binance library


## ApiProgram
- [x] SignUp            -> All field from User Model.
- [x] SignIn            -> Username or Email and Password.
- [x] Auth with email   -> generate key and send for user email.
- [ ] Forget Password   -> send key for userEmail for change passwd.
- [x] Generate ApiToken -> Generate and Save Token in Token Model for User.
- [ ] register_view     -> optimize ( email must be seperated method. )
- [ ] verification      -> check working
## Gateway Models
- [x] User              -> id, username, fullname, email, password.
- [x] Token             -> id, Userid, title, description,Token,is_active.
- [x] EmailAuth         -> id, userid, key, is_forget_pswd, is_active.

## Core Binance
- Maybe deleted and use python-binance library in every single file.