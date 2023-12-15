-- File utils.lua
local function getDataFromRedis(key)
    -- Import redis
    local redis = require "resty.redis"

    -- Create connect to redis
    local red = redis:new()

    -- Set the connection options
    red:set_timeout(1000)

    -- Connect to Redis
    local connect, err = red:connect("127.0.0.1", 6379)
    if not connect then
        ngx.say("Failed to connect to Redis: ", err)
        return
    end

    -- Get value
    local value, err = red:get(key)
    if not value then
        ngx.say("Lỗi khi truy vấn Redis: ", err)
        return
    end

    -- Close connect
    red:close()
    return value
end


local function split(str, delimiter)
    local result = {}
    local pattern = string.format("([^%s]+)", delimiter)
    str:gsub(pattern, function(value) table.insert(result, value) end)
    return result
end

return {
    getDataFromRedis = getDataFromRedis,
    split = split
}