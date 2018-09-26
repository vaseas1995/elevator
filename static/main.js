
function reload_window() {
    $("#key_id").find('option').attr("selected",false) ;
    $("#human_name").find('option').attr("selected",false) ;
    window.location.reload();
}

function send_ajax(officeNumber){

    $.ajax({ 
        url: '/entry', 
        type: 'POST', 
        data:  officeNumber,
        success: function(response){ 
            //  alert(response);
             renderTable(response)
        },
        contentType: "application/json",
        dataType: 'json'
        
    })
}

const renderTable = (resposne) => {
    $('#state tbody tr').remove();    
    let res;
    if(resposne.length > 0 ){
        res =  resposne.reduce((acc, val) => {
           return acc + `<tr> 
                        <td>
                            ${val[0]}
                        </td>
                        <td>
                            ${val[1]}
                        </td>
                        <td>
                            ${val[2]}
                        </td>
                        <td>
                            ${val[3]}
                        </td>
                        <td>
                            <button class="table-btn" name="{{log_row[0]}}" >Primit</button>
                        </td>
                   </tr>`
            console.log(val)
            return `acc ${val}`        
        }, ``) 
    }

    console.log(res);

    $('#state tbody').append(res);
}

var office_number;

window.onload = () => {

     $(document).on('click', '.gray', function(){
         const floorId = $(this).text()
         console.log(floorId)
         send_ajax(floorId);
         $("#etaj_nr").text("Etajul "+floorId);
     });

   $(document).on('click', '.table-btn', function(){
    officeNumber = $(this).closest('tr').children().first().text();
    
    send_ajax(officeNumber);
    $(this).closest('tr').remove();

   })


}

const openModalWindow = (val) => {
    console.log(val)
    giveKeys.style.display = "block"
}
const closeModal = (event) => {
    giveKeys.style.display = "none";
}



function moveDoors() {
    var doors = document.getElementsByClassName("door");
    doors[0].classList.toggle('dtransform');
    doors[1].classList.toggle('dtransform');
}

let elevator = {
    buttons: [],
    catchDom() {
        for (let i = 0; i < 8; i++) {
            let obj = {}
            if (i === 0) {
                obj = {
                    light: document.querySelectorAll('.hbtn')[i],
                    button: document.querySelector('[data-id="' + (i + 1) + '"]'),
                    isActive: true,
                    isCurrent: true
                }
            } else {
                obj = {
                    light: document.querySelectorAll('.hbtn')[i],
                    button: document.querySelector('[data-id="' + (i + 1) + '"]'),
                    isActive: false,
                    isCurrent: false
                }
            }
            this.buttons.push(obj)
        }
    },
    render() {},
    init() {
        this.catchDom()
        this.onElevatorBtnClick()
    },
    onElevatorBtnClick() {
        this.buttons.forEach(v => {
            v.button.onclick = this.onElevatorMove.bind(this)
        })
    },
    onElevatorMove(event) {
        console.log(this.text)
        moveDoors();
        let self = this;
        const clickFloorBtn = parseInt(event.target.dataset.id) - 1;
        let currentElevatorPosition;
        this.buttons.filter(v => {
            if (v.isCurrent === true) {
                currentElevatorPosition = v.button.dataset.id
            }
        })
        console.log(currentElevatorPosition);
        this.buttons[+currentElevatorPosition - 1].isCurrent = false;
        this.buttons[+currentElevatorPosition - 1].button.classList.remove('active-btn-press')
        this.buttons[clickFloorBtn].isCurrent = true;
        this.buttons[clickFloorBtn].button.classList.add('active-btn-press')
        if (+currentElevatorPosition - 1 >= clickFloorBtn) {
            this.onElevatorAnimateDown(currentElevatorPosition, clickFloorBtn, self)
        } else {
            // this.buttons[+currentElevatorPosition - 1].light.classList.remove('bon')
            this.onElevatorAnimateUp(currentElevatorPosition, clickFloorBtn, self)
        }
    },
    onElevatorAnimateUp(currentElevatorPosition, clickFloorBtn, self) {
        if (currentElevatorPosition <= clickFloorBtn) {
            setTimeout(() => {
                console.log("moving up 1s", this);
                this.buttons[+currentElevatorPosition - 1].light.classList.remove('bon')
                this.buttons[currentElevatorPosition].light.classList.add('bon')
                self.buttons[currentElevatorPosition].isActive = true;
                return self.onElevatorAnimateUp(+currentElevatorPosition + 1, clickFloorBtn, self);
            }, 1000);
        }
        else { moveDoors(); }
    },
    onElevatorAnimateDown(currentElevatorPosition, clickFloorBtn, self) {
        if (currentElevatorPosition > clickFloorBtn + 1) {
            currentElevatorPosition = +currentElevatorPosition - 1
            setTimeout(() => {
                console.log("moving down 1s");
                this.buttons[currentElevatorPosition].light.classList.remove('bon')
                this.buttons[+currentElevatorPosition - 1].light.classList.add('bon')
                self.buttons[+currentElevatorPosition].isActive = false;
                return self.onElevatorAnimateDown(+currentElevatorPosition, clickFloorBtn, self);
            }, 1000);
        }
        else if (currentElevatorPosition === clickFloorBtn + 1) { moveDoors(); }
    },
}
elevator.init();
