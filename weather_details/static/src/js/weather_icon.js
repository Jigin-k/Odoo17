/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import { useState} from "@odoo/owl";

class SystrayIcon extends Component {
 setup() {
   super.setup(...arguments);
   this.action = useService("action");
    this.state = useState({
      weatherData: null,
      temp : null,
      date: new Date()
    });
 }
 async _onClick() {
   console.log("Hi")
   const response = await fetch('https://api.openweathermap.org/data/2.5/weather?lat=11.25&lon=75.78&appid=9ee4b0fec4718f124211ef2c6580b702')
  .then(response => response.json())
  .then (data => this.state.weatherData = data)
  .then (data => this.state.temp = (data.main.temp/10).toFixed(1))


  .catch(error => console.error(error));
  console.log(this.state.date)
   }
   }

SystrayIcon.template = "weather_icon";
SystrayIcon.components = {Dropdown,DropdownItem};
export const systrayItem = {
 Component: SystrayIcon,
};
registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });
