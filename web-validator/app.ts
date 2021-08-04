import axios from "axios";
import * as Handlebars from "handlebars"
import dotenv from "dotenv";

dotenv.config();

let config = {
    apiPath: process.env.API_PATH
};

class App {
    public uriElement: HTMLInputElement;

    private requestDateElement: HTMLInputElement;

    private inputTypeElement: HTMLInputElement;

    private followLinksElement: HTMLInputElement;

    private fullTMCheckElement: HTMLInputElement;

    private resultElement: HTMLElement;

    private loadingTemplate: string;

    private errorTemplate: string;

    private successTemplate: string;

    private followTemplate: string;

    private submitButton: HTMLButtonElement;

    initialize(){

        this.uriElement = document.getElementById("inputUri") as HTMLInputElement;
        this.requestDateElement = document.getElementById("inputRequestDate") as HTMLInputElement;
        this.inputTypeElement = document.getElementById("inputType") as HTMLInputElement;
        this.followLinksElement = document.getElementById("inputFollowLinks") as HTMLInputElement;
        this.fullTMCheckElement = document.getElementById("inputTMFullCheck") as HTMLInputElement;

        this.resultElement = document.getElementById("result");
        this.loadingTemplate = document.getElementById("loadingTemplate").innerText;
        this.errorTemplate = document.getElementById("errorTemplate").innerHTML;
        this.successTemplate = document.getElementById("successTemplate").innerHTML;
        this.followTemplate = document.getElementById("followTemplate").innerHTML;

        this.submitButton = document.getElementById("submit") as HTMLButtonElement;
        this.submitButton.addEventListener("click", () => {this.submit();});

        Handlebars.registerHelper('equal', function () {
            const args = Array.prototype.slice.call(arguments, 0, -1);
            return args.every(function (expression) {
                return args[0] === expression;
            });
        });

        Handlebars.registerHelper('title-case', function(value){
            return value
                .split(' ')
                .map(s => s[0].toUpperCase() + s.substr(1).toLowerCase())
                .join(' ')
        })
    }

    public submit(){

        let uri = this.uriElement.value;
        let requestDate = this.requestDateElement.value;
        let inputType = this.inputTypeElement.value;
        let followLinks = this.followLinksElement.checked;
        let fullTMCheck = this.fullTMCheckElement.checked;

        let requestParams = {
            datetime: requestDate,
            uri: uri,
            type: inputType,
            followLinks: followLinks,
            fullTMCheck: fullTMCheck
        };

        this.submitButton.disabled = true;
        let source = Handlebars.compile(this.loadingTemplate);
        this.resultElement.innerHTML = source(this.loadingTemplate, {});

        axios.get(config.apiPath,{
            params: requestParams
        }).then(
            result => {
                this.submitButton.disabled = false;
                this.showResult(result.data)
            },
            error => {
                this.submitButton.disabled = false;
                this.showError([{type: error.message, description: "Connection Error"}]);
            });


        return true;

    }

    public showResult(data: {follow: object,errors: Array<object>}){

        if( data.hasOwnProperty("errors")){
            this.showError(data.errors);
        }
        else{
            let mainSource = Handlebars.compile(this.successTemplate);
            let followHtml = "";
            if(data.follow){
                for( const followType of Object.keys(data.follow)){
                    followHtml = data.follow[followType].reduce((accumulator, data) => {
                        let followSource = Handlebars.compile(this.followTemplate);
                        return accumulator + followSource({data: data, type: followType});
                    }, followHtml);
                }
            }
            this.resultElement.innerHTML = mainSource({data: data})+ followHtml;
        }
    }

    public showError(errors){
        let source = Handlebars.compile(this.errorTemplate);
        this.resultElement.innerHTML = source({data: {errors: errors}});
    }
}


let app = new App();
app.initialize();

