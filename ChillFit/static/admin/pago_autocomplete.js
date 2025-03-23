document.addEventListener("DOMContentLoaded", function () {
    let usuarioField = document.querySelector("#id_usuario");
    let planField = document.querySelector("#id_plan_de_trabajo");
    let montoField = document.querySelector("#id_monto");

    if (!usuarioField || !planField || !montoField) {
        console.error("No se encontraron los campos en el formulario del admin.");
        return;
    }

    usuarioField.addEventListener("change", function () {
        let usuarioId = usuarioField.value;

        if (usuarioId) {
            fetch(`/admin/get_plan_pago/${usuarioId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.plan_id) {
                        planField.value = data.plan_id;
                        montoField.value = data.monto;
                    } else {
                        planField.value = "";
                        montoField.value = "";
                    }
                })
                .catch(error => console.error("Error al obtener el plan de pago:", error));
        }
    });
});
