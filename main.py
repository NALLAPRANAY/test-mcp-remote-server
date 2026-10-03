from fastmcp import FastMCP
import os
import random
import json

mcp=FastMCP("test-remote-server")

@mcp.tool()
def add(a:int,b:int)->int:
    """ Add two numbers a and b and return a+b"""
    return a+b

@mcp.tool()
def generate_random(min:int,max:int):
    """ Generate a number between Min and Max Value"""
    return random.randint(min,max)

@mcp.resource("info://server")
def server_info()->str:
    """ Get information about server """
    info={
        "name":"A Simple Caluclator",
        "version":"1.0.0",
        "description":"A basic MCP Server with math tools",
        "tools":["add","generate_random"],
    
    }
    return json.dump(info)

if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)

