import * as React from "react";
import {
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalButton,
  SIZE,
  ROLE,
} from "baseui/modal";
import { Input } from "baseui/input";
import { FormControl } from "baseui/form-control";

import { useCookies } from "react-cookie";
import axios from "axios";
import { Notification, KIND } from "baseui/notification";

import { Button, KIND as ButtonKind } from "baseui/button";

export const NewEntryModal = ({ isOpen, setOpenCb }) => {
  const [cookies, setCookie, removeCookie] = useCookies();
  const [temperature, setTemperature] = React.useState<number>();
  const [humidity, setHumidity] = React.useState<number>();
  const [location, setLocation] = React.useState<string>("");
  const [error, setError] = React.useState<string>("");

  const jwt = cookies.jwt;

  const createEntry = () => {
    axios
      .post(
        `http://localhost:5001/api/weather/`,
        {
          temperature: temperature,
          humidity: humidity,
          location: location,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${jwt}`,
          },
          withCredentials: true,
        }
      )
      .then((res) => {
        // console.log(res.data);
      })
      .catch((error) => {
        console.error(error);
        if (error.response?.data?.message)
          setError(error.response.data.message);
        else setError(error.message);
      });
  };
  const close = () => {
    setOpenCb(false);
  };

  return (
    <Modal
      onClose={() => setOpenCb(false)}
      closeable
      isOpen={isOpen}
      animate
      autoFocus
      size={SIZE.default}
      role={ROLE.dialog}
    >
      <ModalHeader>Create entry</ModalHeader>
      <ModalBody>
        <FormControl label="Temperaturee">
          <Input
            endEnhancer="°C"
            value={temperature}
            onChange={(e) => setTemperature(Number(e.target.value))}
            type="number"
            placeholder="22"
            clearOnEscape
          />
        </FormControl>

        <FormControl label="Humidity">
          <Input
            endEnhancer="%"
            value={humidity}
            type="number"
            onChange={(e) => setHumidity(Number(e.target.value))}
            placeholder="55"
            clearOnEscape
          />
        </FormControl>

        <FormControl label="Where">
          <Input
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="kitchen"
            clearOnEscape
          />
        </FormControl>
        {error && (
          <Notification kind={KIND.negative} closeable>
            {() => error}
          </Notification>
        )}
      </ModalBody>
      <ModalFooter>
        <Button onClick={close} kind={ButtonKind.tertiary}>
          Cancel
        </Button>
        <Button onClick={createEntry}>Create</Button>
      </ModalFooter>
    </Modal>
  );
};
