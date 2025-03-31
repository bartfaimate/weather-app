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

import axios from "axios";
import { Notification, KIND } from "baseui/notification";
import { useCookies } from 'react-cookie';
import { Button, KIND as ButtonKind } from "baseui/button";

export const ModifyEntryModal = ({ isOpen, setOpenCb, entryId }) => {
  const [cookies, setCookie, removeCookie] = useCookies();
  const [temperature, setTemperature] = React.useState<number>();
  const [humidity, setHumidity] = React.useState<number>();
  const [location, setLocation] = React.useState<string>("");
  const [error, setError] = React.useState<string>("");
  const [info, setInfo] = React.useState<string>("");

  const isLoggedIn = cookies.loggedIn ?? false

  React.useEffect(() => {
    setError("");
    setInfo("");
    getEntry();
  }, [entryId, isOpen]);

  const jwt = cookies.jwt;
  

  const getEntry = () => {
    axios
      .get(`http://localhost:5001/api/weather/${entryId}/`)
      .then((res) => {
        setTemperature(res.data.temperature);
        setHumidity(res.data.humidity);
        setLocation(res.data.location);
      })
      .catch((error) => {
        if (error.response?.data?.message)
          setError(error.response.data.message);
        else setError(error.message);
      });
  };

  const deleteEntry = () => {
    axios
      .delete(`http://localhost:5001/api/weather/${entryId}/`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwt}`,
        },
        withCredentials: true,
      })
      .then((res) => {
        setInfo("Entry removed");
      })
      .catch((error) => {
        if (error.response?.data?.message)
          setError(error.response.data.message);
        else setError(error.message);
      });
  };

  const updateEntry = () => {
    axios
      .put(
        `http://localhost:5001/api/weather/${entryId}/`,
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
        console.log(res.data);
        setInfo("Entry successfully updated");
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
      <ModalHeader>Modify entry {entryId}</ModalHeader>
      <ModalBody>
        <FormControl label="Temperature">
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
        {info && (
          <Notification kind={KIND.positive} closeable>
            {() => info}
          </Notification>
        )}
      </ModalBody>
      <ModalFooter>
        <Button onClick={close} kind={ButtonKind.tertiary}>
          Cancel
        </Button>
        { isLoggedIn && <Button onClick={updateEntry}>Modify</Button>}
        {isLoggedIn && <Button onClick={deleteEntry} kind={ButtonKind.secondary}>Remove</Button>}
      </ModalFooter>
    </Modal>
  );
};
