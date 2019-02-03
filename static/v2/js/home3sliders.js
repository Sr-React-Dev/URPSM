$(window).load(function() {
    $("#flexiselDemo1").flexisel();
    $("#flexiselDemo2").flexisel({
        visibleItems: 3,
        itemsToScroll: 1,
        animationSpeed: 400,
        infinite: true,
        navigationTargetSelector: null,
        autoPlay: {
            enable: false,
            interval: 5000,
            pauseOnHover: true
        },
        responsiveBreakpoints: { 
            portrait: { 
                changePoint:480,
                visibleItems: 1,
                itemsToScroll: 1
            }, 
            landscape: { 
                changePoint:640,
                visibleItems: 2,
                itemsToScroll: 2
            },
            tablet: { 
                changePoint:0,
                visibleItems: 2,
                itemsToScroll: 2
            }
        }
    });
    $("#flexiselDemo3").flexisel({
        visibleItems: 3,
        itemsToScroll: 1,
        animationSpeed: 200,
        infinite: true,
        navigationTargetSelector: null,
        autoPlay: {
            enable: false,
            interval: 5000,
            pauseOnHover: true
        },
        responsiveBreakpoints: { 
            portrait: { 
                changePoint:480,
                visibleItems: 1,
                itemsToScroll: 1
            }, 
            landscape: { 
                changePoint:640,
                visibleItems: 2,
                itemsToScroll: 2
            },
            tablet: { 
                changePoint:0,
                visibleItems: 2,
                itemsToScroll: 2
            }
        }
    });
    
    $("#flexiselDemo4").flexisel({
        visibleItems: 5,
        itemsToScroll: 1,
        animationSpeed: 200,
        infinite: true,
        navigationTargetSelector: null,
        autoPlay: {
            enable: false,
            interval: 5000,
            pauseOnHover: true
        },
        responsiveBreakpoints: { 
            portrait: { 
                changePoint:480,
                visibleItems: 2,
                itemsToScroll: 2
            }, 
            landscape: { 
                changePoint:640,
                visibleItems: 4,
                itemsToScroll: 2
            },
            tablet: { 
                changePoint:0,
                visibleItems: 4,
                itemsToScroll: 2
            }
        }
    });   
    
});