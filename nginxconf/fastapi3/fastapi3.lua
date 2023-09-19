-- fastapi3.lua
-- package.path = package.path .. ";/usr/local/openresty/lualib/ngx/fastapi3/?.lua"

local utils = require "utils"
local getDataFromRedis = utils.getDataFromRedis
local split = utils.split

-- local host = ngx.var.host
local host = "hieudomain1.com"
local str_host = tostring(host)
local domain = getDataFromRedis(str_host)

-- Xu ly data
local str = tostring(domain)
local delimiter = "|"
local parts_origin = split(str, delimiter)
local protocol = parts_origin[1]
local host_upstr = parts_origin[2]
local address = parts_origin[3]

ngx.say("protocol: ", protocol)
ngx.say("host_upstr: ", host_upstr)
ngx.say("address: ", address)

-- ngx.var.backend = protocol.."://"..address
-- ngx.header["Foo"] = "Bar"



