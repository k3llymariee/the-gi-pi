const pad = (n) => {
    if (n < 10) {
        return '0' + n
    } else {
        return n
    }
};

const defaultTime = () => {

    const currentDate = new Date();
    const date = currentDate.getDate();
    const month = currentDate.getMonth() + 1;  //January is 0 not 1
    const year = currentDate.getFullYear();
    const hours = currentDate.getHours();
    const minutes = currentDate.getMinutes();

    // The format is "yyyy-MM-ddThh:mm"

    const currentDateTime  = pad(year) + "-" + pad(month) + "-" + pad(date)
        + "T" + pad(hours) + ":" + pad(minutes);

    $('#symptom_time').val(currentDateTime);
}

defaultTime();