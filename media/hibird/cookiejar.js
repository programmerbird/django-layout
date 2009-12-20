/*
**	Cookiejar.js v1.2 - A Javascript class for storing and accessing cookies 
**	Copyright (C) 2004 frantik - email: frizzantik@yahoo.com
**	
**	This program is free software; you can redistribute it and/or modify it under 
**	the terms of the GNU General Public License as published by the Free Software 
**	Foundation; either version 2 of the License, or (at your option) any later 
**	version.
**	
**	This program is distributed in the hope that it will be useful, but WITHOUT ANY 
**	WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
**	PARTICULAR PURPOSE. See the GNU General Public License for more details.
**	
** 
**  ++ Revision History
**  v1.2 - Prepared for distribution
**  v1.1 - Domain, path and secure properties added
**	v1.0 - Original version
**
**
**	++ Methods exposed by the cookiejar:
**	
**	- cookiejar(cookieJarName)
**	This is the constructor.  cookieJarName is the name of the collection of 
**	cookies you would like to associate with this object
**	
**	- doesExist(id)
**	Returns false if id does not exist in the jar.  
**  Returns the position in the jar of id if does exist
**	
**	- delCookie(id)
**	Removes id from the jar
**	
**	- setCookie(id, value)
**	Sets id to value
**	
**	- getCookie(id)
**	Returns the value of id
**	
**	- setExpiration(years, days, hours, minutes, seconds, milliseconds) 
**	Set the jar to expire in years + days + hours + minutes + seconds + milliseconds
**
**	- read()
**	Reads the cookies from disk into the jar
**	
**	- write() 
**	Writes the cookies in the jar to disk
**	
**	- reset()
**	Removes all cookies from the jar
**
**
**	++ The following properties are exposed by cookiejar:
**
**	path - the path of the cookie.  Default is null.
**  domain - the domain of the cookie.  Default is null.
**	expiration - how man milliseconds until the cookie will expire. Default is 1 year.
**	secure - indicates if the cookie requires a secure transmission.  Default is false
**
**
**	++ The following properties are exposed but need not be accessed directly:
**	
**	jar - string with all cookie information
**  jarname - the name of the jar
**  divider - string which divides id-value pairs in jar
**  divider2 - string which divides the id from the value in id-value pairs in the jar
**
**
*/

function cookiejar (jarname)
{
	this.jar = "";
	this.jarname = jarname;
	this.expiration = 1 * 365 * 24 * 60 * 60 * 1000;
	this.divider = "#";
	this.divider2 = ":";
	this.path = null;
	this.domain = null;
	this.secure = false;

	this.doesExist = c_doesExist;	
	this.delCookie = c_delCookie;
	this.setCookie = c_setCookie;
	this.getCookie = c_getCookie;
	this.read	= c_read;
	this.write = c_write;
	this.reset = c_reset;
	this.setExpiration = c_setExpiration;
	
	this.read();

}

function c_doesExist(c_id)
{	if (c_id == "") return false;
	return this.jar.indexOf(escape(c_id) + this.divider2);
}

function c_delCookie(c_id)
{	
	exists = this.doesExist(c_id);
	if (exists == -1) return false;
	
	var end = this.jar.indexOf(this.divider,exists);
	if (end == -1)
		end = this.jar.length
	else
		end;

	this.jar = this.jar.substring(0,exists-1) + this.jar.substring(end,this.jar.length);
		
	return true;
}
		
		
function c_setCookie(c_id, c_value)
{	this.delCookie(c_id);
	this.jar += this.divider + escape(c_id) + this.divider2 + escape(c_value) ;
	return true;
}

function c_getCookie(c_id)
{	
	exists = this.doesExist(c_id);
	if (exists == -1) return null;
	
	tempjar = this.jar.substring(exists,this.jar.length);

	var end = tempjar.indexOf(this.divider);
	if (end == -1)
		end = tempjar.length
	
	tempjar = tempjar.substring(0,end);

	var tempArr = tempjar.split(this.divider2);

	if (unescape(tempArr[0]) != c_id)
		return null;

	return unescape(tempArr[1]);		

}

function c_read()
{
  var dc = document.cookie;
  var prefix = this.jarname + "=";
  var begin = dc.indexOf("; " + prefix);
  if (begin == -1) {
    begin = dc.indexOf(prefix);
    if (begin != 0) return "";
  } else
    begin += 2;
  var end = document.cookie.indexOf(";", begin);
  if (end == -1)
    end = dc.length;
  this.jar =  unescape(dc.substring(begin + prefix.length, end));

  return true;
}

function c_reset()
{
	this.jar = "";
	this.write();
}


function c_write()
{

	var dateObj = new Date();
	dateObj.setTime(dateObj.getTime() + this.expiration);

	var base = new Date(0);
    var skew = base.getTime();
    if (skew > 0)
       dateObj.setTime(dateObj.getTime() - skew);


	document.cookie = this.jarname + "=" + escape(this.jar) +
				"; expires=" + dateObj.toGMTString() + 
				  ((this.path == null)   ? "" : "; path=" + this.path) +
				  ((this.domain == null) ? "" : "; domain=" + this.domain) +
				  ((this.secure) ? "; secure" : "");

				

	return true;

}

function c_setExpiration(years, days, mins, secs, mill)
{

	 this.expiration = (((years) ? (years) : 1) * 365 * 60 * 60 * 1000) +
	  				   (((days)  ? (days)  : 365) * 60 * 60 * 1000) +
					   (((mins)  ? (mins)  : 60) * 60 * 1000 ) +
					   (((secs)  ? (secs)  : 60) * 1000) +
					   ((mill)  ? (mill)   : 1000);
}

