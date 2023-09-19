-- fastapi3.lua
-- Import thư viện Redis Lua
local redis = require "resty.redis"

-- Tạo một đối tượng Redis
local red = redis:new()

local host = ngx.var.host


local str_host = tostring(host)
-- Thiết lập kết nối Redis
local ok, err = red:connect("127.0.0.1", 6379)

if not ok then
    ngx.status = ngx.HTTP_INTERNAL_SERVER_ERROR
    ngx.say("Lỗi khi kết nối tới Redis: ", err)
    ngx.exit(ngx.status)
end

-- Truy vấn Redis để lấy địa chỉ IP
local ip, err = red:get(str_host)
if not ip then
    ngx.status = ngx.HTTP_INTERNAL_SERVER_ERROR
    ngx.say("Lỗi khi truy vấn Redis: ", err)
    ngx.exit(ngx.status)
end

-- fuction split
function split(str, delimiter)
    local result = {}
    local pattern = string.format("([^%s]+)", delimiter)
    str:gsub(pattern, function(value) table.insert(result, value) end)
    return result
end


-- Xu ly data
if ip then
    -- set data
    local str = tostring(ip)
    local delimiter = "|"
    local parts = split(str, delimiter)
    local protocol = parts[1]
    local host_upstr = parts[2]
    local address = parts[3]

    ngx.var.backend = protocol.."://"..address
    ngx.header["Foo"] = "Bar"
    -- CHECK RESULT
    -- ngx.say("protocol: ", protocol)
    -- ngx.say("host: ", host)
    -- ngx.say("address: ", address)
    -- ngx.say("Kết nối Redis: ",protocol.."://"..address)
end


-- Đóng kết nối Redis
local ok, err = red:set_keepalive(10000, 100)
if not ok then
    ngx.status = ngx.HTTP_INTERNAL_SERVER_ERROR
    ngx.say("Lỗi khi đóng kết nối Redis: ", err)
    ngx.exit(ngx.status)
end
