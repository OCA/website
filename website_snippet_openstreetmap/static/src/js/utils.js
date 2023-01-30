odoo.define("website_snippet_openstreetmap.utils", function () {
    "use strict";

    function generateOpenStreetMapLink(coordinates, dataset) {
        if (coordinates) {
            var earthRadius = 6378137;

            var area = parseFloat(dataset.mapZoom);
            var offset = area / 2;

            var minlon =
                coordinates[1] +
                (-offset / (earthRadius * Math.cos((Math.PI * coordinates[0]) / 180))) *
                    (180 / Math.PI);
            var minlat = coordinates[0] + (-offset / earthRadius) * (180 / Math.PI);
            var maxlon =
                coordinates[1] +
                (offset / (earthRadius * Math.cos((Math.PI * coordinates[0]) / 180))) *
                    (180 / Math.PI);
            var maxlat = coordinates[0] + (offset / earthRadius) * (180 / Math.PI);

            const url =
                "https://www.openstreetmap.org/export/embed.html?bbox=" +
                encodeURIComponent(
                    minlon + "," + minlat + "," + maxlon + "," + maxlat
                ) +
                "&marker=" +
                encodeURIComponent(coordinates[0] + "," + coordinates[1]) +
                "&layer=" +
                dataset.mapType;

            return url;
        }
        return "";
    }

    return {
        generateOpenStreetMapLink: generateOpenStreetMapLink,
    };
});
