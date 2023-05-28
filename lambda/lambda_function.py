# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import requests
import random
import ask_sdk_core.utils as ask_utils

from imdb import IMDb
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_slot_value

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to FlickFate, my functionalities are: Recommend a movie, In which streaming service can you find a movie, And give a random phrase from a movie. You can test me by saying: Recommend me a movie"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class quoteIntentHandler(AbstractRequestHandler):
    """Handler for quote Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("quote")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        url = "https://andruxnet-random-famous-quotes.p.rapidapi.com/"
        querystring = {"cat":"movies","count":"1"}
        headers = {
            "X-RapidAPI-Key": "da318c225cmshe652ecbca62d7eap1544aejsnc2850b6bac62",
            "X-RapidAPI-Host": "andruxnet-random-famous-quotes.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        quote = data[0]["quote"]
        movie = data[0]["author"]
        
        # Save the movie title in the session attributes
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["movie"] = movie

        speak_output = f"{quote} from the movie {movie}"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
class streamingIntentHandler(AbstractRequestHandler):
    """Handler for streaming Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("streaming")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slot_value = get_slot_value(handler_input, "movie")

        url = "https://streaming-availability.p.rapidapi.com/v2/search/title"
        querystring = {
            "title": slot_value,
            "country": "mx",
            "show_type": "movie",
            "output_language": "en"
        }
        headers = {
            "X-RapidAPI-Key": "da318c225cmshe652ecbca62d7eap1544aejsnc2850b6bac62",
            "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        streaming_services = data["result"][0]["streamingInfo"]["mx"]
        all_services = ", ".join(streaming_services)

        speak_output = f"The movie '{slot_value}' is available on the following services: {all_services}."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like to find another movie?")
                .response
        )


class pelicula_randomIntentHandler(AbstractRequestHandler):
    """Handler for pelicula random Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("pelicula_random")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        ia = IMDb()
        movies = ia.get_top250_movies()
        random_movie = random.choice(movies)
        title = random_movie['title']
        
        speak_output = title

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like another random movie?")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "How can I help? My functionalities are: Recommend a movie, In which streaming service can you find a movie, And give a random phrase from a movie. You can test me by saying: Recommend me a movie"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. My functionalities are: Recommend a movie, In which streaming service can you find a movie, And give a random phrase from a movie. You can test me by saying: Recommend me a movie"
        reprompt = "I didn't catch that. My functionalities are: Recommend a movie, In which streaming service can you find a movie, And give a random phrase from a movie.?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. My functionalities are: Recommend a movie, In which streaming service can you find a movie, And give a random phrase from a movie."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(quoteIntentHandler())
sb.add_request_handler(streamingIntentHandler())
sb.add_request_handler(pelicula_randomIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()