'use strict';

function urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

async function confirm_process(tag) {
    const f_d = new FormData();
    f_d.append("data", tag);
    f_d.append("id", "ON_2023");

    await fetch("https://ondaily.pythonanywhere.com/data_process/crypto_security/event_encrypt", {
        method: "POST",
        body: f_d,
    }).then(res => res.text()).then(data =>{

        });

}
async function update_token_process(token_new) {
    const form_data = new FormData();
    form_data.append("data", token_new);

    await fetch("https://ondaily.pythonanywhere.com/data_process/crypto_security/event_encrypt/update_token", {
        method: "POST",
        body: form_data,
    }).then(res => res.text()).then(data =>{
        console.log("CAMBIO DE LLAVE RESPUESTA");
        if (data){
            return true;
        }else{
            return false;
        }
    });
}

self.addEventListener('push', function(event) {
    const data_for_notify = event.data.json();
    const title = data_for_notify.title_notify;

    const options = {
        body: data_for_notify.message_notify,
        icon: data_for_notify.icon_notify,
        badge: data_for_notify.badge_notify,
        image: data_for_notify.image_notify,
        vibrate: data_for_notify.vibrate_notify,
        tag: data_for_notify.data_notify,
    };

    event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    const tag = event.notification.tag;
    const notificationData = JSON.parse(tag);
    const IDNotify = notificationData.id;
    const link_redirect = notificationData.redirectTo;

    confirm_process(tag)

    if (link_redirect.length > 0){
         event.waitUntil(
            self.clients.matchAll({ type: 'window' }).then(clients => {
                const client = clients.find(c => c.visibilityState === 'visible');
                if (client) {
                    return client.navigate(link_redirect);
                } else {
                    return self.clients.openWindow(link_redirect);
                }
            })
         );
    }


});


self.addEventListener('pushsubscriptionchange', function(event) {
    update_token_process("DATA NEW");
    event.waitUntil(

            // self.registration.pushManager.getSubscription()
            // .then(function(newSubscription) {
            //     if (newSubscription) {
            //         // update_token_process();
            //         // Enviar la nueva suscripción al servidor
            //     } else {
            //       // La suscripción se ha revocado, realiza las acciones necesarias
            //         // handleRevokedSubscription();
            //     }
            // })
            // .catch(function(error) {
            //     console.error('Error en la resuscripción:', error);
            // });

    );
});

// COMPROBACION ABAJO

self.addEventListener('periodicsync', function(event) {
    if (event.tag === 'update_token_process_fun') {
        // Realizar las acciones de sincronización aquí
        update_token_process("token_new");

    }
});


self.addEventListener('activate', (event) => {

});




