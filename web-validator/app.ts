import axios from "axios";
import * as Mustache from "mustache"

class App {
    public uriElement: HTMLInputElement;

    private requestDateElement: HTMLInputElement;

    private inputTypeElement: HTMLInputElement;

    private followLinksElement: HTMLInputElement;

    private fullTMCheckElement: HTMLInputElement;

    private resultElement: HTMLElement;

    private errorTemplate: string;

    private successTemplate: string;

    private submitButton: HTMLButtonElement;

    initialize(){

        this.uriElement = document.getElementById("inputUri") as HTMLInputElement;
        this.requestDateElement = document.getElementById("inputRequestDate") as HTMLInputElement;
        this.inputTypeElement = document.getElementById("inputType") as HTMLInputElement;
        this.followLinksElement = document.getElementById("inputFollowLinks") as HTMLInputElement;
        this.fullTMCheckElement = document.getElementById("inputTMFullCheck") as HTMLInputElement;

        this.resultElement = document.getElementById("result");
        this.errorTemplate = document.getElementById("errorTemplate").innerHTML;
        this.successTemplate = document.getElementById("successTemplate").innerHTML;

        this.submitButton = document.getElementById("submit") as HTMLButtonElement;
        this.submitButton.addEventListener("click", () => {this.submit();});
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

        axios.get("http://labs.mementoweb.org/validator/",{
            params: requestParams
        }).then(
            result => {
                this.submitButton.disabled = false;
                this.showResult(result.data)
            },
            error => {
                console.log(error);
                this.showError();
            });

        return true;

    }

    public showResult(data: object){

        if( data.hasOwnProperty("errors")){
            this.resultElement.innerHTML = Mustache.render(this.errorTemplate, {data: data});
        }
        else{
            this.resultElement.innerHTML = Mustache.render(this.successTemplate, {data: data});
        }
    }

    public showError(){
        this.requestDateElement.innerHTML = "Error, Please try again."
    }
}


let app = new App();
app.initialize();

