import axios from "axios";
import * as Mustache from "mustache"

class App {
    public uriElement: HTMLInputElement;

    private requestDateElement: HTMLInputElement;

    private defaultTGElement: HTMLInputElement;

    private inputTypeElement: HTMLInputElement;

    private resultElement: HTMLElement;

    private errorTemplate: string;

    private successTemplate: string;

    private submitButton: HTMLButtonElement;

    initialize(){

        this.uriElement = document.getElementById("inputUri") as HTMLInputElement;
        this.requestDateElement = document.getElementById("inputRequestDate") as HTMLInputElement;
        this.defaultTGElement = document.getElementById("inputDefaultTimegate") as HTMLInputElement;
        this.inputTypeElement = document.getElementById("inputType") as HTMLInputElement;

        this.resultElement = document.getElementById("result");
        this.errorTemplate = document.getElementById("errorTemplate").innerHTML;
        this.successTemplate = document.getElementById("successTemplate").innerHTML;

        this.submitButton = document.getElementById("submit") as HTMLButtonElement;
        this.submitButton.addEventListener("click", () => {this.submit();});
    }

    public submit(){

        let uri = this.uriElement.value;
        let requestDate = this.requestDateElement.value;
        let defaultTimegate = this.defaultTGElement.value;
        let inputType = this.inputTypeElement.value;

        let requestParams = {
            // datetime: requestDate,
            // uri: uri,
            // type: inputType,
            // timegate: defaultTimegate
        };
        this.submitButton.disabled = true;
        axios.get("http://labs.mementoweb.org/validator/",{
            params: requestParams
        }).then(
            result => this.showResult(result.data),
            error => console.log("error"));

        return true;

    }

    public showResult(data: object){
        console.log(data);
        this.submitButton.disabled = false;
        if( data.hasOwnProperty("errors")){
            this.resultElement.innerHTML = Mustache.render(this.errorTemplate, {data: data});
        }
        else{
            this.resultElement.innerHTML = Mustache.render(this.successTemplate, {data: data});
        }
    }
}


let app = new App();
app.initialize();

